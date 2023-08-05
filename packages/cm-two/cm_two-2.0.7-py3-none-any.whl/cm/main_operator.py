import _tkinter
import datetime
import subprocess
import os
import traceback
from cm.modules import *
import threading
import pickle
from time import sleep
from cm.wlistener import WListener
from cm.configs import config as s
from cm.styles import fonts
from ar_qdk.main import ARQDK
from cm.gcore_interaction import db_functions as db_funcs
from orup_errors.main import OrupErrorsManager
from cm.video_worker import start_video_stream
import sys
from qpi.main import QPI
from PIL import Image, ImageTk
import io


class Operator:
    """ Основной оператор взaимодействия между окнами, его экземляр
    распределяется между всеми модулями и используются
    для их взаимной обработки """

    def __init__(self, root, settings, scale, can, deffaultScreenSize,
                 loadingcan, ar_ip, ar_port=52250, scale_server_ip=None,
                 scale_server_port=2297, fgsm=False, cm_cams_info=None):
        # Словарь, где будут хранится номера считанных авто, время считывания,
        # Сколько раз была отмена и т.д
        self.orup_black_list = {}
        self.root = root
        self.fgsm = fgsm
        self.currentPage = None
        self.cm_cams_info = cm_cams_info
        self.status_ready = False
        self.if_show_weight = True
        self.current = 'main'
        self.unfinished_records = []
        self.loadingcan = loadingcan
        self.loading_repcentage = 0
        self.deffaultScreenSize = deffaultScreenSize
        self.current = 'main'
        self.settings = settings
        self.ar_ip = ar_ip
        self.ar_qdk = ARQDK(ar_ip, int(ar_port))
        # self.ar_qdk_reciever = ARQDK(ar_ip, int(52251))
        while True:
            try:
                self.ar_qdk.make_connection()
                self.ar_qdk.subscribe()
                self.ar_qdk.get_data()
                # $self.ar_qdk_reciever.make_connection()
                self.loadingcan.delete('no_connection_info')
                break
            except ConnectionRefusedError:
                self.no_ar_connection()
                sleep(3)
        self.set_cam_info(
            self.ar_qdk.execute_method('get_cams', get_response=True)['info'])
        self.general_tables_dict = {}
        self.get_wdb_tables_info()
        self.terminal = Terminal(root, settings, self, can)
        if self.settings.mirrored:
            self.auto_exit_x, self.auto_exit_y = 1615, 852
            self.gross_x, self.gross_y = 417, 852
        else:
            self.auto_exit_x, self.auto_exit_y = 417, 852
            self.gross_x, self.gross_y = 1615, 852
        self.auto_cams_width, self.auto_cams_height = 420, 360
        self.terminal.launchingOperations()
        self.main_btns_drawn = False
        self.exitFlag = False
        self.road_anim_info = {self.settings.exit_gate: {'pos': 0, 'img': ...,
                                                         'busy': False},
                               self.settings.entry_gate: {'pos': 0, 'img': ...,
                                                          'busy': False},
                               'active': False}
        self.animation = 'off'

        self.scale = scale
        if not scale_server_ip:
            scale_server_ip = ar_ip
        self.wr = WListener(ip=s.wrip, port=s.wrport, ar_ip=scale_server_ip,
                            scale_port=scale_server_port)
        self.aborted = False
        self.userRole = 'moder'
        ###################### PAGES ###################################
        self.authWin = AuthWin(root, settings, self, can)
        self.mainPage = MainPage(root, settings, self, can)
        self.statPage = Statistic(root, settings, self, can)
        self.sysNot = SysNot(root, settings, self, can)
        self.manual_gate_control = ManualGateControl(root, settings, self, can)
        #########################LAUNCHING##############################
        self.authWin.openWin()
        threading.Thread(target=self.wr.scale_reciever,
                         args=(scale_server_ip,), daemon=True).start()
        #threading.Thread(target=self.scaleRecieving,
        #                 args=(),
        #                 daemon=True).start()  # Запуск демона для обработки показания весов
        threading.Thread(target=self.ar_reciever_thread, args=(),
                         daemon=True).start()
        # Данные для рисования грузовика на весовой платформе
        self.orup_error_manager = OrupErrorsManager(canvas=self.terminal.can,
                                                    types_list=self.get_trash_types_reprs(),
                                                    cats_list=self.get_trash_cats_reprs(),
                                                    text_color=cs.orup_error_txt_color,
                                                    debtors_list=[],
                                                    carriers_list=self.get_clients_reprs(),
                                                    objects_list=self.get_table_reprs(
                                                        'pol_objects'))
        self.gcore_status = True
        self.create_qpi()
        root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.create_video_streams()

    def turn_cams(self, on=True, cam_type=None):
        for cam in self.cameras_info:
            if not cam['enable'] or not self.get_cam_cm_enable(cam):
                continue
            if cam_type:
                if cam['type'] == cam_type:
                    cam["video_worker_inst"].can_show = on
            else:
                cam["video_worker_inst"].can_show = on

    def get_cam_ip(self, ar_cam_info):
        """ Чекнуть, не задан ли IP камеры в СМ, если нет - взять с АР"""
        cam_ip = self.cm_cams_info[ar_cam_info['type']]['ip']
        if not cam_ip:
            cam_ip = ar_cam_info['ip']
        return cam_ip

    def get_cam_port(self, ar_cam_info):
        """ Чекнуть, не задан ли IP камеры в СМ, если нет - взять с АР"""
        cam_ip = self.cm_cams_info[ar_cam_info['type']]['port']
        if not cam_ip:
            cam_ip = ar_cam_info['rtsp_port']
        return cam_ip

    def get_cam_cm_enable(self, ar_cam_info):
        """ Чекнуть, не задан ли IP камеры в СМ, если нет - взять с АР"""
        return self.cm_cams_info[ar_cam_info['type']]['enable']

    def create_video_streams(self):
        for cam in self.cameras_info:
            if cam['type'] == 'main' and cam['enable'] and self.get_cam_cm_enable(cam):
                cam_ip = self.get_cam_ip(cam)
                port = self.get_cam_port(cam)
                inst = start_video_stream(self.root, self.terminal.can,
                                          xpos=417, ypos=280,
                                          v_width=420,
                                          v_height=400,
                                          cam_login=cam['login'],
                                          cam_pass=cam['pw'],
                                          cam_ip=cam_ip,
                                          cam_port=port,
                                          zoom_callback_func=self.terminal.cam_zoom_callback,
                                          hide_callback_func=self.terminal.cam_hide_callback,
                                          zoomed_y=self.terminal.h/2,
                                          zoomed_x=self.terminal.w/2,
                                          cam_type=cam['type'],
                                          zoomed_video_height=600,
                                          zoomed_video_width=1500)
                cam['video_worker_inst'] = inst
            if cam['type'] == 'cad_gross' and cam['enable'] and self.get_cam_cm_enable(cam):
                cam_ip = self.get_cam_ip(cam)
                port = self.get_cam_port(cam)
                inst = start_video_stream(self.root, self.terminal.can,
                                          xpos=self.gross_x, ypos=self.gross_y,
                                          v_width=self.auto_cams_width,
                                          cam_port=port,
                                          v_height=self.auto_cams_height,
                                          cam_login=cam['login'],
                                          cam_pass=cam['pw'],
                                          cam_ip=cam_ip,
                                          zoom_callback_func=self.terminal.cam_zoom_callback,
                                          hide_callback_func=self.terminal.cam_hide_callback,
                                          zoomed_y=self.terminal.h / 2,
                                          zoomed_x=self.terminal.w / 2,
                                          cam_type=cam['type'],
                                          zoomed_video_height=600,
                                          zoomed_video_width=1500)
                cam['video_worker_inst'] = inst
            if cam['type'] == 'auto_exit' and cam['enable'] and self.get_cam_cm_enable(cam):
                cam_ip = self.get_cam_ip(cam)
                port = self.get_cam_port(cam)
                inst = start_video_stream(self.root, self.terminal.can,
                                          xpos=self.auto_exit_x,
                                          ypos=self.auto_exit_y,
                                          v_width=self.auto_cams_width,
                                          cam_port=port,
                                          v_height=self.auto_cams_height,
                                          cam_login=cam['login'],
                                          cam_pass=cam['pw'],
                                          cam_ip=cam_ip,
                                          zoom_callback_func=self.terminal.cam_zoom_callback,
                                          hide_callback_func=self.terminal.cam_hide_callback,
                                          zoomed_y=self.terminal.h / 2,
                                          zoomed_x=self.terminal.w / 2,
                                          cam_type=cam['type'],
                                          zoomed_video_height=600,
                                          zoomed_video_width=1500)
                cam['video_worker_inst'] = inst

    def create_qpi(self):
        self.qpi = QPI('0.0.0.0', 50505, without_auth=True,
                       mark_disconnect=False,
                       core=self, auto_start=False)
        qpi_thread = threading.Thread(target=self.qpi.launch_mainloop,
                                      daemon=True)
        qpi_thread.start()

    def get_api_support_methods(self):
        methods = {'zoom_app': {'method': self.terminal.set_window_normal},
                   'close_app': {'method': self.closeApp},
                   'reboot': {'method': self.reboot}}
        return methods


    def recieve_ar_responses(self):
        response = self.ar_qdk.get_data()
        if not response:
            print("ERROR")
            return response
        # if 'info' in response.keys():
        #    response = response['info'][0]
        try:
            core_method = response['core_method']
            method_result = response['info']
            return core_method, method_result
        except KeyError:
            print("ERROR")
            pass

    def recieve_ar_responses_two(self, ar_qdk):
        response = ar_qdk.get_data()
        if not response:
            return response
        try:
            core_method = response['core_method']
            method_result = response['info']
            return core_method, method_result
        except KeyError:
            print("ERROR")

            pass

    def null_weight(self):
        self.ar_qdk.execute_method('set_null_weight')

    def closeApp(self):
        threading.Thread(target=self.close_app_thread(), daemon=True).start()

    def close_app_thread(self):
        """ Функция выполняющая завершающие операции, при закрытии программы """
        self.ar_qdk.capture_cm_terminated()
        self.ar_qdk.restart_unit()
        self.root.destroy()
        sleep(2.5)
        sys.exit(0)

    def ar_reciever_thread(self):
        while True:
            response = self.recieve_ar_responses()
            if not response:
                raise AttributeError
            else:
                core_method, method_result = response
                self.operate_ar_response(core_method, method_result)

    def operate_ar_response(self, core_method, method_result):
        if core_method == 'get_unfinished_records':
            if method_result['status'] == 'success':
                self.operate_get_unfinished_records(method_result['info'])
            else:
                self.mainPage.tar.clearTree()
        if core_method == 'update_round_status':
            self.update_status_operate(method_result)
        elif core_method == 'cad_callback':
            self.cad_work(method_result)
        elif core_method == 'get_cams':
            self.set_cam_info(method_result['info'])
        elif core_method == 'get_last_event' and method_result[
            'status'] == 'success':
            self.operate_last_event(**method_result['info'][0])
        elif core_method == 'faultDetected':
            self.terminal.errors += [{'level1': method_result['info']}]
        elif core_method == 'try_auth_user':
            if method_result['status'] == 'success':
                self.try_login(method_result['info'][0]['auth_status'],
                               method_result['info'][0]['id'])
            else:
                self.authWin.incorrect_login_act()
        elif core_method == 'get_history':
            self.operate_get_history(method_result['status'],
                                     method_result['info'])
        elif core_method == 'get_table_info':
            self.operate_table_info(s.tables_info, self.general_tables_dict,
                                    method_result['tablename'],
                                    method_result['info'])
        elif core_method == 'update_table':
            self.operate_table_info(s.tables_info, self.general_tables_dict,
                                    method_result['tablename'],
                                    method_result['info'],
                                    loading=False)
        elif core_method == 'update_gate_status':
            self.operate_gate_changes_command(**method_result)
        elif core_method == 'update_cm':
            self.update_cm(**method_result)
        elif core_method == 'close_cm':
            self.closeApp()
        elif core_method == 'draw_auto_exit_with_pic' and self.ifORUPcanAppear(
                None):
            self.draw_auto_exit_with_pic(picture=method_result['picture'],
                                         course=method_result['course'])
            # self.draw_auto_exit_pic(method_result['picture'])
        elif core_method == 'car_detected' and self.ifORUPcanAppear(
                method_result['carnum']):
            self.car_detected_operate(auto_id=method_result['auto_id'],
                                      client_id=method_result['client_id'],
                                      carrier_id=method_result['last_carrier'],
                                      trash_cat_id=method_result[
                                          'last_trash_cat'],
                                      trash_type_id=method_result[
                                          'last_trash_type'],
                                      course=method_result['course'],
                                      have_gross=method_result['have_gross'],
                                      car_protocol=method_result[
                                          'car_protocol'],
                                      polygon=method_result['last_polygon'],
                                      car_number=method_result['carnum'],
                                      pol_object=method_result['pol_object'],
                                      last_tare=method_result['last_tare'],
                                      car_read_client_id=method_result[
                                          'car_read_client_id'],
                                      photo=method_result['photo'])
        elif core_method == 'get_health_monitor':
            self.operate_get_health_monitor(method_result)
        elif core_method == 'get_status':
            self.operate_get_status(method_result)

    def cad_work(self, info):
        self.cad_activate_time = datetime.datetime.now()
        if ((self.current != 'MainPage' and self.current != 'ManualGateControl')
                or self.currentPage.blockImgDrawn or self.terminal.cam_zoom):
           return
        text = 'ДВИЖЕНИЕ'
        if info['cam_type'] == 'cad_gross':
            x = self.gross_x - self.auto_cams_width/2
            y = self.gross_y - self.auto_cams_height/2 + 60
            self.terminal.can.create_text(x+350,y-16, text=text,
                                          tag='cad_color',
                                          fill="#F5B85E",
                                          font=fonts.cad_work_font)
        else:
            x = self.auto_exit_x - self.auto_cams_width/2
            y = self.auto_exit_y - self.auto_cams_height/2 + 60
            self.terminal.can.create_text(x+65,y-16, text=text,
                                          tag='cad_color',
                                          fill="#F5B85E",
                                          font=fonts.cad_work_font)
        threading.Thread(target=self.cad_color_remover).start()

    def cad_color_remover(self):
        while True:
            if datetime.datetime.now() - self.cad_activate_time > datetime.timedelta(seconds=5):
                self.terminal.can.delete('cad_color')
                break
            sleep(1)


    def draw_auto_exit_with_pic(self, course, picture):
        if course == "OUT":
            self.currentPage.orupActExit(carnum='deff', call_method="auto",
                                         course=course, with_pic=picture)
        else:
            threading.Thread(target=self.draw_auto_entrance_pic,
                             args=(picture,)).start()
            self.currentPage.orupAct(call_method='unknown_number')

    def draw_auto_exit_pic(self, picture):
        img = Image.open(io.BytesIO(picture))
        im_r = img.crop((int(1920 / 2 - 700), int(1080 / 2 - 200),
                         int(1920 / 2 + 500), int(1080 / 2 + 400)))
        img_byte_arr = io.BytesIO()
        im_r.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        self.photoimg = ImageTk.PhotoImage(
            Image.open(io.BytesIO(img_byte_arr)))
        self.currentPage.can.create_image(self.terminal.w / 2,
                                          self.terminal.h / 3,
                                          image=self.photoimg,
                                          tags=('orupentry',))
        self.currentPage.can.create_text(self.terminal.w / 2,
                                         self.terminal.h / 10,
                                         text='система не распознала гос.номер авто',
                                         font=fonts.date_font, fill='white',
                                         tags=('orupentry',))

    def draw_auto_entrance_pic(self, picture):
        img = Image.open(io.BytesIO(picture))
        #im_r = img.crop((1100, 400, 2350, 1150))
        im_r = img.crop((500, 400, 1050, 1100))
        img_byte_arr = io.BytesIO()
        im_r.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        self.photoimg = ImageTk.PhotoImage(
            Image.open(io.BytesIO(img_byte_arr)))
        self.currentPage.can.create_image(self.terminal.w / 6.4,
                                          self.terminal.h / 2,
                                          image=self.photoimg,
                                          tags=('orupentry',))
        # self.currentPage.can.create_text(self.terminal.w/2, self.terminal.h/10,
        #                                 text='система не распознала гос.номер авто',
        #                                 font=fonts.date_font, fill='white',
        #                                 tags=('orupentry',))

    def operate_get_status(self, status, *args, **kwargs):
        """ Получить статус GCore"""
        self.gcore_status = status
        if status == 'locked':
            self.terminal.block_gravity()

    def operate_get_health_monitor(self, health_monitor: dict, *args,
                                   **kwargs):
        """ От GCore пришел словарь, содержащий информацию типа health_monitor"""
        self.terminal.check_gcore_health(health_monitor)
        self.sysNot.tar.fillTree(health_monitor)

    def operate_last_event(self, trash_cat, trash_type, carrier, no_exit,
                           client_id, object, polygon,
                           *args, **kwargs):
        """ От AR пришла информация о последнем заезде авто """
        carrier = self.get_client_repr(carrier)
        trash_cat = self.get_trash_cat_repr(trash_cat)
        trash_type = self.get_trash_type_repr(trash_type)
        client = self.get_client_repr(client_id)
        pol_object = self.get_pol_object_repr(object)
        platform = self.get_polygon_platform_repr(polygon)
        self.currentPage.contragentCombo.set(self.validate_last_event(carrier))
        self.currentPage.trashCatOm.set(self.validate_last_event(trash_cat))
        self.currentPage.trashTypeOm.set(self.validate_last_event(trash_type))

        self.currentPage.platform_choose_combo.set(
            self.validate_last_event(platform, message='Выберите площадку'))
        self.currentPage.objectOm.set(self.validate_last_event(pol_object,
                                                               message='Выберите объект размещения'))
        if self.currentPage.clientOm.state() and \
                self.currentPage.clientOm.state()[0] == 'disable':
            pass
        else:
            self.currentPage.clientOm.set(
                self.validate_last_event(client,
                                         message='Выберите клиента (плательщика)'))

        self.currentPage.no_exit_var.set(no_exit)

    def validate_last_event(self, num, message=0):
        if num:
            return num
        else:
            return message

    def operate_gate_changes_command(self, gate_name, status, *args, **kwargs):
        """ Обработчик команды от GCore об изменении положении стрелы шлагбаума """
        if gate_name == 'entry' and status == 'open':
            print('Внешний открывается')
            self.terminal.open_entry_gate_operation_start()
        elif gate_name == 'entry' and status == 'close':
            print('Внешний закрывается')
            self.terminal.close_entry_gate_operation_start()
        elif gate_name == 'exit' and status == 'open':
            print('Внутренний открывается')
            self.terminal.open_exit_gate_operation_start()
        elif gate_name == 'exit' and status == 'close':
            print('Внутренний закрывается')
            self.terminal.close_exit_gate_operation_start()

    def update_cm(self, new_version=None):
        command = 'pip3 install --upgrade cm_two'
        if new_version:
            command += f'=={new_version}'
        command += ' --no-cache-dir'
        os.system(command)
        self.create_update_text()

    def create_update_text(self):
        self.terminal.can.create_text(self.terminal.w / 2,
                                      self.terminal.h / 20,
                                      text='ДОСТУПНО ОБНОВЛЕНИЕ! ПЕРЕЗАПУСТИТЕ ПРИЛОЖЕНИЕ!',
                                      fill='white',
                                      font=fonts.loading_status_font)

    def operate_table_info(self, tables_info, general_tables_dict, tablename,
                           result, loading=True, *args, **kwargs):
        """ Когда пришли данные от GCore о содержимом таблицы tablename """
        # Получаем репрезентативное значние
        repr_value = tables_info[tablename]['repr']
        # Отформатировать данные, что бы получить данные типа {'repr':{col1:1'val1'}, 'repr':{'col2': val2}}
        formated = self.format_wdb_table_info(result, keyname=repr_value)
        # Добавить в словарь, содержащие содержимое всех таблиц инфу вида {'tablename': {repr: {...}, repr: {...} }}
        general_tables_dict[tablename] = formated
        if loading:
            self.create_loading_info(tablename, self.loadingcan)
        elif tablename == 'clients':
            self.orup_error_manager.all_args['carriers'] = self.get_clients_reprs()

    def create_loading_info(self, tablename, loadingcan):
        try:
            loadingcan.delete('loading_status')
            self.loading_repcentage += 100 / len(s.tables_info.keys())
            loading_percentage = str(int(self.loading_repcentage)) + '%'
            loadingcan.create_text(self.root.winfo_screenwidth() / 2,
                                   self.root.winfo_screenheight() / 2 * 1.32,
                                   text=s.tables_info[tablename][
                                       'loading_description'],
                                   font=fonts.loading_status_font,
                                   fill='white',
                                   tags=('loading_info', 'loading_status'))
            loadingcan.create_text(self.root.winfo_screenwidth() / 2,
                                   self.root.winfo_screenheight() / 2,
                                   text=loading_percentage,
                                   font=fonts.loading_percents_font,
                                   fill='white',
                                   tags=('loading_info', 'loading_status'))
        except _tkinter.TclError:
            pass

    def format_wdb_table_info(self, result: list, keyname: str, *args,
                              **kwargs):
        """ Создаем словарь, где ключом будет keyname записи, а значением - вся информация по записи
        (тоже в виде словаря)"""
        formated = {}
        for record in result:
            key = record[keyname]
            formated[key] = record
        return formated

    def operate_get_unfinished_records(self, info, *args, **kwargs):
        self.mainPage.tar.clearTree()
        try:
            self.unfinished_records = info
            self.fill_current_treeview(info)
            self.currentPage.tar.sortId(self.currentPage.tree, '#0',
                                        reverse=True)
        except:
            traceback.format_exc()

    def fill_current_treeview(self, info):
        first = False
        for rec in info:
            if not rec['time_out'] or first:
                rec['trash_cat'] = self.get_trash_cat_repr(rec['trash_cat'])
                self.mainPage.tar.fillTree(id=rec['id'], brutto=rec['brutto'],
                                           tara=rec['tara'],
                                           cargo=rec['cargo'],
                                           time_in=rec['time_in'],
                                           trash_cat=rec['trash_cat'],
                                           car_number=rec['car_number'],
                                           notes=rec['full_notes'])
            else:
                rec['trash_cat'] = self.get_trash_cat_repr(rec['trash_cat'])
                self.mainPage.tar.fillTree(id=rec['id'], brutto=rec['brutto'],
                                           tara=rec['tara'],
                                           cargo=rec['cargo'],
                                           time_in=rec['time_in'],
                                           trash_cat=rec['trash_cat'],
                                           car_number=rec['car_number'],
                                           notes=rec['full_notes'],
                                           tags=('evenrow',))
                first = True

    def operate_get_history(self, status, records):
        """ От GCore пришел список, содержащий информацию обо всех заездов за запрашиваемый период в виде словарей """
        self.statPage.tar.clearTree()
        self.statPage.weight_sum = 0
        self.statPage.records_amount = 0
        self.statPage.uncount_records = []
        if status == 'success':
            for record in records:
                self.statPage.tar.insertRec(id=record['record_id'],
                                            car_number=record['car_number'],
                                            carrier=self.get_client_repr(
                                                record.pop('carrier')),
                                            brutto=record['brutto'],
                                            tara=record['tara'],
                                            cargo=record['cargo'],
                                            trash_cat=self.get_trash_cat_repr(
                                                record.pop('trash_cat')),
                                            trash_type=self.get_trash_type_repr(
                                                record.pop('trash_type')),
                                            auto=self.get_auto_repr(
                                                record.pop('auto')),
                                            time_in=record['time_in'],
                                            time_out=record['time_out'],
                                            notes=record['full_notes'],
                                            client=self.get_client_repr(
                                                record.pop('client_id')))
                self.statPage.history[record['record_id']] = record
                if record['cargo']:
                    self.statPage.weight_sum += record['cargo']
                    self.statPage.records_amount += 1
                if record['tara'] == 0:
                    self.statPage.uncount_records.append(record['record_id'])
        try:
            self.currentPage.tar.sortId(self.currentPage.tree, '#0',
                                        reverse=True)
        except:
            pass
        # Разместить итоговую информацию (общий тоннаж и количество взвешиваний)
        self.statPage.place_amount_info(self.statPage.weight_sum,
                                        self.statPage.records_amount,
                                        tag='amount_info')

    def operate_ar_sys_info(self, info):
        for k, v in info.items():
            if k == 'data' and 'Внешний' in v and 'открывается.' in v:
                print('Внешний открывается')
                self.terminal.open_entry_gate_operation_start()
            elif k == 'data' and 'Внешний' in v and 'закрывается.' in v:
                print('Внешний закрывается')
                self.terminal.close_entry_gate_operation_start()
            elif k == 'data' and 'Внутренний' in v and 'открывается.' in v:
                print('Внутренний открывается')
                self.terminal.open_exit_gate_operation_start()
            elif k == 'data' and 'Внутренний' in v and 'закрывается.' in v:
                print('Внутренний закрывается')
                self.terminal.close_exit_gate_operation_start()

    def update_status_operate(self, info):
        # Если получена команда на обновление статуса заезда
        self.status_ready = False
        self.road_anim_info['active'] = True
        if str(info['notes']).strip() == 'Запись обновлена':
            self.updateMainTree()
        try:
            for k, v in info.items():
                self.road_anim_info[k] = v
            if info['status'] == 'Начало взвешивания':
                self.currentPage.destroyORUP('total')
            if (info[
                'status'].strip() == 'Ожидание пересечения фотоэлементов.'):
                self.mainPage.make_abort_active()
            if (info['protocol'].strip() == 'Машина заезжает.' or info[
                'protocol'].strip() == 'Машина выезжает.'):
                self.updateMainTree()
            self.drawStatus()
            if (
                    self.current == 'MainPage' or self.current == 'ManualGateControl') and not self.currentPage.blockImgDrawn:
                self.drawCarMoving()
            if (info['status'].strip() == 'Протокол завершен'
                    or info['status'].strip() == 'Время истекло!'
                    or info['status'].strip() == 'Заезд прерван вручную!'):
                self.operateStatusEnd()
        except:
            print(traceback.format_exc())
            pass

    def draw_road_anim(self):
        if self.road_anim_info['active']:
            self.drawCarMoving()
            self.drawStatus()

    def car_detected_operate(self, auto_id: int, client_id: int,
                             trash_cat_id: int, trash_type_id: int,
                             course: str, have_gross: bool, car_protocol,
                             polygon: id, pol_object: int, carrier_id: int,
                             car_number: str = None, last_tare=None,
                             car_read_client_id=None, photo=None,
                             **kwargs):
        # Если получена команда на открытие ОРУП
        self.currentPage.orupState = True
        # Получить репрезентативные значения по ID
        client_repr = self.get_client_repr(client_id)
        carrier_repr = self.get_client_repr(carrier_id)
        trash_cat_repr = self.get_trash_cat_repr(trash_cat_id)
        trash_type_repr = self.get_trash_type_repr(trash_type_id)
        auto_repr = self.get_auto_repr(auto_id)
        if not auto_repr:
            auto_repr = car_number
        polygon = self.get_polygon_repr(polygon)
        pol_object = self.get_pol_object_repr(pol_object)
        self.currentPage.car_protocol = car_protocol

        if have_gross:
            # Если брутто взвешено, вывести ОРУП-тара
            self.currentPage.orupActExit(carnum=auto_repr, call_method="auto",
                                         course=course)
        else:
            # Если же нет (надо инициировать заезд), вывести ОРУП-брутто
            call_method = "auto"
            if photo:
                call_method = 'photo'
                threading.Thread(target=self.draw_auto_entrance_pic,
                                 args=(photo,)).start()
            self.currentPage.orupAct(carnum=auto_repr, contragent=carrier_repr,
                                     trashType=trash_type_repr,
                                     trashCat=trash_cat_repr,
                                     call_method=call_method,
                                     car_protocol=car_protocol,
                                     course=course, polygon=polygon,
                                     pol_object=pol_object,
                                     client=client_repr,
                                     last_tare=last_tare,
                                     car_read_client_id=car_read_client_id
                                     )

    def fetch_if_record_init(self, carnum):
        active_cars = self.terminal.get_cars_inside()
        if carnum in active_cars:
            return True

    def fetch_car_protocol(self, carnum):
        try:
            car_protocol = self.general_tables_dict[s.auto_table][carnum][
                'id_type']
        except KeyError:
            car_protocol = 'tails'
        return car_protocol

    def open_entry_gate(self):
        self.ar_qdk.operate_gate_manual_control(operation='open',
                                                gate_name='entry')

    def close_entry_gate(self):
        self.ar_qdk.operate_gate_manual_control(operation='close',
                                                gate_name='entry')

    def open_exit_gate(self):
        self.ar_qdk.operate_gate_manual_control(operation='open',
                                                gate_name='exit')

    def close_exit_gate(self):
        self.ar_qdk.operate_gate_manual_control(operation='close',
                                                gate_name='exit')

    def ifORUPcanAppear(self, car_number):
        # Возвращает TRUE, если можно нарисовать окно ОРУП
        if (self.currentPage and self.current != 'AuthWin'
                and self.current != 'ManualGateControl'
                and self.status_ready and not self.currentPage.blockImgDrawn
                and self.orup_blacklist_can_init(car_number)):
            return True
        else:
            return False

    def getInfoFromDict(self, info, target):
        # Получить зачение словаря с информацией о команде по ключу
        goal = info[target]
        if goal == 'none':
            goal = 'Неизвестно'
        return goal

    def operateStatusEnd(self):
        '''Обработчик завершения заезда авто'''
        sleep(2)
        self.currentPage.can.delete('mtext', 'car_icon')
        self.status_ready = True
        self.road_anim_info['active'] = False
        self.mainPage.make_abort_unactive()

    def updateMainTree(self, mode='usual'):
        '''Обновить таблицу текущих записей'''
        if self.current == 'MainPage' and self.mainPage.orupState == False:
            self.mainPage.updateTree()
            if mode == 'create':
                self.mainPage.drawMainTree()

    def getData(self, sock):
        '''Получает сериализированные данные и возвращает их в исходную форму'''
        data = sock.recv(4096)
        if data: data = pickle.loads(data)
        return data

    def getOrupMode(self, course, id_type):
        '''Определить атрибут, передаваемый ОРУПу, согласно курсу движения авто'''
        mode = '_'.join((id_type, course))
        return mode

    def drawStatus(self):
        '''Рисует статус заезда текстом при заезде-выезде на главном меню'''
        self.mainPage.can.delete('mtext')
        if self.current == 'MainPage' and self.mainPage.orupState == False:
            notes = f"Гос. номер:\n{self.road_anim_info['carnum']}\n" \
                    f"Cтатус:\n{self.road_anim_info['status']}\n"
            if self.road_anim_info['notes']:
                notes += f"Примечания:\n{self.road_anim_info['notes']}\n"
            self.mainPage.can.create_text(self.terminal.w / 9.15,
                                          self.terminal.h / 2.72,
                                          text=notes, font=fonts.status_text,
                                          tags=('mtext', 'statusel'), fill='#BABABA',
                                          anchor=NW)

    def drawCarMoving(self):
        '''Рисует грузовик на грузовой платформе при инициировании протокола
		заезда или выезда на главном меню'''
        self.car_protocol = self.road_anim_info['protocol']
        self.car_direction = self.road_anim_info['course']

        car_direction_txt = self.road_anim_info['face']
        cur_pos_txt = self.road_anim_info['pos']

        cur_pos_cm = self.settings.car_poses[cur_pos_txt]
        obj = self.settings.car_face_info[car_direction_txt]
        obj = self.terminal.getAttrByName(obj)
        self.drawCarIcon(obj, cur_pos_cm)

    def drawCarIcon(self, obj, poses):
        self.mainPage.can.delete('car_icon')
        self.mainPage.can.create_image(poses, image=obj[3], anchor=NW,
                                       tag='car_icon')

    def try_login(self, status, id, *args, **kwargs):
        """ Обрабатывает результат авторизации от GravityCore """
        if status:
            self.current_userid = id
            self.currentPage.drawToolbar()
            self.authWin.rebinding()
            self.mainPage.openWin()
            self.status_ready = True
            if not self.currentPage.clockLaunched:
                self.currentPage.start_clock()
                self.currentPage.clockLaunched = True

    def get_gcore_status(self):
        # Запросить статус GCore
        self.ar_qdk.get_status()

    def close_record(self, record_id):
        """ Закрыть незаконченную запись (только раунд брутто) """
        self.ar_qdk.close_opened_record(record_id=record_id)
        self.currentPage.destroyBlockImg()

    def cancel_tare(self, record_id):
        self.ar_qdk.cancel_tare(record_id=record_id)
        self.currentPage.destroyBlockImg()

    def open_new_page(self, page):
        try:
            self.currentPage.page_close_operations()
        except:
            pass
        self.current = page.name
        self.currentPage = page

    def get_polygon_platforms_reprs(self, table_name=s.polygon_objects_table):
        """ Вернуть репрезентативные значения из таблицы организаций-пользователей весовой площадкой """
        return self.get_table_reprs(table_name)

    def get_polygon_platform_id(self, polygon_repr):
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.polygon_objects_table,
                                             polygon_repr)

    def get_polygon_object_id(self, object_repr):
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             'pol_objects',
                                             object_repr)

    def get_pol_object_repr(self, pol_object_id):
        """ Вернуть репрезентативные значения из таблицы юзеров """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             'pol_objects', pol_object_id)

    def get_pol_objects_reprs(self):
        """ Вернуть репрезентативные значения из таблицы pol_objects"""
        return self.get_table_reprs('pol_objects')

    def get_polygon_platform_repr(self, pol_platform_id):
        """ Вернуть репрезентативные значения из таблицы юзеров """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.polygon_objects_table,
                                             pol_platform_id)

    def get_auto_reprs(self, auto_table=s.auto_table):
        """ Вернуть репрезентативные значения из таблицы авто """
        return self.get_table_reprs(auto_table)

    def get_auto_repr(self, auto_id):
        """ Вернуть репрезентативные значения из таблицы юзеров """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.auto_table, auto_id)

    def get_auto_id(self, auto_repr):
        """ Вернуть id юзера с репрезегтативным значением auto_repr"""
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.auto_table, auto_repr)

    def get_users_reprs(self, users_table=s.users_table):
        """ Вернуть репрезентативные значения из таблицы users"""
        return self.get_table_reprs(users_table)

    def get_user_repr(self, user_id):
        """ Вернуть репрезентативные значения из таблицы юзеров """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.users_table, user_id)

    def get_user_id(self, user_repr):
        """ Вернуть id юзера с репрезегтативным значением user_repr"""
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.users_table, user_repr)

    def get_trash_types_reprs(self, trash_types_table=s.trash_types_table):
        """ Вернуть все репрезентативные значения из таблицы видов грузов """
        return self.get_table_reprs(trash_types_table)

    def get_trash_type_repr(self, trash_type_id):
        """ Вернуть репрезентативное название trash_type по его id """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.trash_types_table,
                                             trash_type_id)

    def get_polygon_repr(self, polygon_id):
        """ Вернуть репрезентативное название полигона по его id """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.polygon_objects_table,
                                             polygon_id)

    def get_trash_type_id(self, type_name):
        """ Вернуть id вида груза type_name"""
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.trash_types_table, type_name)

    def get_trash_cats_reprs(self, trash_cats_table=s.trash_cats_table):
        """ Вернуть репрезентативные значения из таблицы категорий грузов """
        return self.get_table_reprs(trash_cats_table)

    def get_trash_cat_repr(self, trash_cat_id):
        """ Вернуть репрезентативное название trash_cat по его id """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.trash_cats_table,
                                             trash_cat_id)

    def get_trash_cat_id(self, cat_name):
        """ Вернуть id категории груза cat_name"""
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.trash_cats_table,
                                             cat_name)

    def get_clients_reprs(self, clients_table=s.clients_table):
        """ Вернуть все репрезентативные значения из таблицы Клиенты"""
        return self.get_table_reprs(clients_table)

    def get_client_repr(self, client_id):
        """ Вернуть репрезентативное название client по его id """
        return db_funcs.get_repr_by_id_table(self.general_tables_dict,
                                             s.clients_table, client_id)

    def get_client_id(self, client):
        """ Вернуть id клиента client"""
        return db_funcs.get_id_by_repr_table(self.general_tables_dict,
                                             s.clients_table, client)

    def get_table_reprs(self, table_name):
        """ Вернуть репрезентативные (понтятные для людей) значения из таблицы tablename
         ( например cat_name из trash_cats) """
        return db_funcs.get_table_rerps(self.general_tables_dict, table_name)

    def get_trashtypes_by_trashcat_repr(self, trash_cat_repr):
        """ Вернуть список видов грузов, у которых trash_cat = trash_cat_repr[id]"""
        trash_types = db_funcs.get_trashtypes_by_trashcat_repr(
            self.general_tables_dict, s.trash_types_table,
            s.trash_cats_table, trash_cat_repr)
        return trash_types

    def get_gcore_health_monitor(self):
        """ Получить состояние GCore """
        self.ar_qdk.get_health_monitor()

    def get_wdb_tables_info(self):
        """ Сохранить все данные таблиц wdb в словарь вида {tablename0: [info0, info1], tablename1: [info4, info[2]}"""
        for tablename in list(s.tables_info.keys()):
            self.ar_qdk.get_table_info(table_name=tablename)
            while True:
                # response = self.recieve_ar_responses()
                response = self.recieve_ar_responses_two(self.ar_qdk)
                if response:
                    core_method, method_result = response
                    if core_method == 'get_table_info':
                        self.operate_ar_response(core_method, method_result)
                        break

    def no_ar_connection(self):
        """ Если нет подключения к AR """
        self.loadingcan.delete('no_connection_info')
        self.loadingcan.create_text(self.root.winfo_screenwidth() / 2,
                                    self.root.winfo_screenheight() / 2,
                                    text='Не удалось подключиться к ядру...'
                                         '\nПерезапуск...',
                                    font=fonts.loading_status_font,
                                    fill='white',
                                    anchor='s',
                                    justify='center',
                                    tags=('no_connection_info'))

    def orup_blacklist_new_car(self, car_num):
        self.orup_black_list[car_num] = {'declines': 1,
                                         'last_decline': datetime.datetime.now()}

    def orup_blacklist_increment(self, car_num):
        self.orup_black_list[car_num]['declines'] += 1
        self.orup_black_list[car_num]['last_decline'] = datetime.datetime.now()

    def orup_blacklist_del(self, car_num):
        try:
            self.orup_black_list.__delitem__(car_num)
        except KeyError:
            pass

    def orup_blacklist_can_init(self, car_number):
        """ Проверить, есть ли авто в blacklist и можно ли открыть для него
        ОРУП """
        try:
            blacklist_info = self.orup_black_list[car_number]
            if datetime.datetime.now() > (blacklist_info['last_decline']
                                          + datetime.
                                                  timedelta(0, 3)
                                          * blacklist_info['declines']):
                return True
        except KeyError:
            return True

    def set_cam_info(self, info):
        print(info)
        new_l = []
        for cam in info:
            cam['zoomed'] = False
            new_l.append(cam)
        self.cameras_info = new_l


    def reboot(self):
        command = 'systemctl reboot'
        command = "echo {}|sudo -S {}".format('Assa+123', command)
        os.system(command)
