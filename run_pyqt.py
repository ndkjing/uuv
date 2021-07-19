# coding:utf-8
import sys
import os
import time
from ui import main_ui, setting_ui, angle
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
# from vtk import *
# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
from stl import mesh
import pyqtgraph.opengl as gl

from dataManager import data_manager
import config
from storage import save_data


class SettingWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = setting_ui.Ui_Form()
        self.ui.setupUi(self)


class WorkerThread(QThread):
    finish = pyqtSignal(int)

    def __init__(self, parent=None, run_func=None):
        super().__init__(parent)
        self.run_func = run_func

    def run(self):
        self.run_func()

class Camera:
    """摄像头对象"""

    def __init__(self, url, out_label):
        """初始化方法"""
        self.url = url
        self.outLabel = out_label

    def display(self):
        """显示"""
        cap = cv2.VideoCapture(self.url)
        start_time = time.time()
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if (time.time() - start_time) > 0.1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    self.outLabel.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    start_time = time.time()

class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.datamanager_obj = data_manager.DataManager()
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_data)
        self.timer.timeout.connect(self.update_base_info)
        self.timer.start(100)
        self.timer1 = QTimer()  # 定时器
        self.timer1.timeout.connect(self.update)
        self.timer1.start(1000)  # 每1s 更新一次
        # 显示视频
        self.open_flag = True
        self.painter = QPainter(self)
        self.front_video_stream = None
        self.back_video_stream = None
        self.front_video_stream = cv2.VideoCapture(config.front_video_src)
        self.back_video_stream = cv2.VideoCapture(config.back_video_src)
        # 显示三维模型
        # self.currentSTL = None
        # self.lastDir = None
        # self.droppedFilename = None
        # self.viewer = gl.GLViewWidget()
        # self.ui.view_layout.addWidget(self.viewer, 1)
        # self.show_view()
        self.label1 = angle.Clock_paint()
        self.ui.verticalLayout_2.addWidget(self.label1)
        # 设置页面
        self.setting_dlg = SettingWindow()
        # 绑定修改数据
        self.connect_single_slot()
        # 前摄后后摄图片
        self.frame_front = None
        self.frame_back = None

        # 长时间的工作放到这里
        # self.tcp_work = WorkerThread(parent=None, run_func=self.datamanager_obj.tcp_server_obj.wait_connect)
        # self.work.finish.connect(self.showResult)
        # self.tcp_work.start()
        self.joystick_work = WorkerThread(parent=None, run_func=self.datamanager_obj.joystick_obj.get_data)
        self.joystick_work.finish.connect(self.showResult)
        self.joystick_work.start()
        # 更新pid参数
        self.update_pid(value=None)

    # 绑定信号和槽
    def connect_single_slot(self):
        # 显示设置页面
        self.ui.setting_btn.clicked.connect(self.setting_dlg.show)
        # 先打开本地保存的pid设置
        self.ui.setting_btn.clicked.connect(self.update_pid)
        # 修改设置数据
        self.ui.setting_btn.clicked.connect(self.update_setting_data)
        # 打开关闭tcp服务和打开关闭遥控
        self.setting_dlg.ui.close_server_btn.clicked.connect(self.close_server)
        self.setting_dlg.ui.start_server_btn.clicked.connect(self.start_server)
        self.setting_dlg.ui.start_joystick_btn.clicked.connect(self.start_joystick)
        self.setting_dlg.ui.close_joystick_btn.clicked.connect(self.close_joystick)
        # pid参数改变
        self.setting_dlg.ui.h_p_slider.valueChanged.connect(self.update_pid)
        self.setting_dlg.ui.h_i_slider.valueChanged.connect(self.update_pid)
        self.setting_dlg.ui.h_d_slider.valueChanged.connect(self.update_pid)
        self.setting_dlg.ui.v_p_slider.valueChanged.connect(self.update_pid)
        self.setting_dlg.ui.v_i_slider.valueChanged.connect(self.update_pid)
        self.setting_dlg.ui.v_d_slider.valueChanged.connect(self.update_pid)
        # 截图录像相关
        self.ui.front_camera_cap.clicked.connect(self.front_cap_info)
        self.ui.front_camera_video.clicked.connect(self.front_video_info)
        self.ui.back_camera_cap.clicked.connect(self.back_cap_info)
        self.ui.back_camera_video.clicked.connect(self.back_video_info)
        # 使能电机
        self.ui.init_motor_btn.clicked.connect(self.init_motor)

    def showResult(self):
        print('show result')
        self.joystick_work = WorkerThread(parent=None, run_func=self.datamanager_obj.joystick_obj.get_data)
        self.joystick_work.finish.connect(self.showResult)
        self.joystick_work.start()

    # 跟新pid参数
    def update_pid(self, value):
        sender = self.sender()
        update = True
        if sender == self.setting_dlg.ui.h_p_slider:
            self.setting_dlg.ui.h_p_label.setText('h_p:' + str(value / 10.0))
            self.datamanager_obj.pid[0] = float(value / 10.0)
        elif sender == self.setting_dlg.ui.h_i_slider:
            self.setting_dlg.ui.h_i_label.setText('h_i:' + str(value / 10.0))
            self.datamanager_obj.pid[1] = float(value / 10.0)
        elif sender == self.setting_dlg.ui.h_d_slider:
            self.setting_dlg.ui.h_d_label.setText('h_d:' + str(value / 10.0))
            self.datamanager_obj.pid[2] = float(value / 10.0)
        elif sender == self.setting_dlg.ui.v_p_slider:
            self.setting_dlg.ui.v_p_label.setText('v_p:' + str(value / 10.0))
            self.datamanager_obj.pid_v[0] = float(value / 10.0)
        elif sender == self.setting_dlg.ui.v_i_slider:
            self.setting_dlg.ui.v_i_label.setText('v_i:' + str(value / 10.0))
            self.datamanager_obj.pid_v[0] = float(value / 10.0)
        elif sender == self.setting_dlg.ui.v_d_slider:
            self.setting_dlg.ui.v_d_label.setText('v_d:' + str(value / 10.0))
            self.datamanager_obj.pid_v[0] = float(value / 10.0)
        else:
            if not self.datamanager_obj.joystick_obj.b_connect:
                self.datamanager_obj.joystick_obj.init_joystick()
            update = False
            data = save_data.get_data(config.save_pid_path)
            if data:
                self.datamanager_obj.pid = data.get('h_pid')
                self.datamanager_obj.pid_v = data.get('v_pid')
                self.setting_dlg.ui.h_p_label.setText('h_p:' + str(self.datamanager_obj.pid[0]))
                self.setting_dlg.ui.h_p_slider.setValue(int(self.datamanager_obj.pid[0] * 10))
                self.setting_dlg.ui.h_i_label.setText('h_i:' + str(self.datamanager_obj.pid[1]))
                self.setting_dlg.ui.h_i_slider.setValue(int(self.datamanager_obj.pid[1] * 10))
                self.setting_dlg.ui.h_d_label.setText('h_d:' + str(self.datamanager_obj.pid[2]))
                self.setting_dlg.ui.h_d_slider.setValue(int(self.datamanager_obj.pid[2] * 10))
                self.setting_dlg.ui.v_p_label.setText('v_p:' + str(self.datamanager_obj.pid_v[0]))
                self.setting_dlg.ui.v_p_slider.setValue(int(self.datamanager_obj.pid_v[0] * 10))
                self.setting_dlg.ui.v_i_label.setText('v_i:' + str(self.datamanager_obj.pid_v[1]))
                self.setting_dlg.ui.v_i_slider.setValue(int(self.datamanager_obj.pid_v[1] * 10))
                self.setting_dlg.ui.v_d_label.setText('v_d:' + str(self.datamanager_obj.pid_v[2]))
                self.setting_dlg.ui.v_d_slider.setValue(int(self.datamanager_obj.pid_v[2] * 10))
        if update:
            data = {'h_pid': self.datamanager_obj.pid, 'v_pid': self.datamanager_obj.pid_v}
            save_data.set_data(data, config.save_pid_path)

    # 更新显示消息
    def update_setting_data(self):
        self.setting_dlg.ui.ip_address_label.setText(str(self.datamanager_obj.tcp_server_obj.bind_ip + \
                                                         ':' + str(self.datamanager_obj.tcp_server_obj.bind_port)))

        self.setting_dlg.ui.joystick_label.setText('遥控:' + str(self.datamanager_obj.joystick_obj.count))

    def start_server(self):
        print('start_server')

    def close_server(self):
        self.datamanager_obj.tcp_server_obj.close()
        print('close_server')

    def start_joystick(self):
        print('start_server')
        # print(self.datamanager_obj.joystick_obj.b_connect)
        # if not self.datamanager_obj.joystick_obj.b_connect:
        #     self.datamanager_obj.joystick_obj.init_joystick()
        #     print(self.datamanager_obj.joystick_obj.count)
        #     if self.datamanager_obj.joystick_obj.count >= 1:
        #         self.joystick_work = WorkerThread(parent=None, run_func=self.datamanager_obj.joystick_obj.get_data)
        #         # self.work.finish.connect(self.showResult)
        #         self.joystick_work.start()

    def close_joystick(self):
        # TODO
        print('close_joystick')

    # 发送数据
    def send_data(self):
        if self.datamanager_obj.tcp_server_obj.b_connect:
            self.datamanager_obj.send_tcp_data(b_once=True)

    # 更新基础数据
    def update_base_info(self):
        if self.datamanager_obj.joystick_obj.b_connect == 1:
            self.ui.joystick_label.setText("遥控")
        else:
            self.ui.joystick_label.setText("无遥控")
        self.ui.deep_label.setText("深度:13.5m")
        self.ui.pressure_label.setText("压力:1.6")
        self.ui.temperature_label.setText("水温:29.8")
        self.ui.leak_label.setText("未漏水")

    # 获取保存数据路径
    def get_path(self, b_save_img=True, b_front=True):
        """
        :param b_save_img: 保存图片
        :param b_front: 前摄
        :return:
        """
        str_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        if b_save_img:
            if b_front:
                save_path = os.path.join(config.save_imgs_dir, str_time + 'front_.jpg')
            else:
                save_path = os.path.join(config.save_imgs_dir, str_time + 'back_.jpg')
        else:
            if b_front:
                save_path = os.path.join(config.save_imgs_dir, str_time + 'front_.mp4')
            else:
                save_path = os.path.join(config.save_imgs_dir, str_time + 'back_.mp4')
        return save_path

    # 前摄截图提示
    def front_cap_info(self):
        save_path = self.get_path()
        self.save_img(front=True, save_path=save_path)
        reply = QMessageBox.question(self, '提示', '截图成功，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)

    # 后摄截图提示
    def back_cap_info(self):
        save_path = self.get_path(b_front=False)
        self.save_img(front=False, save_path=save_path)
        reply = QMessageBox.question(self, '提示', '截图成功，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)

    # 前摄录像提示
    def front_video_info(self):
        save_path = self.get_path(b_save_img=False)
        self.save_video(front=True, start=True)
        reply = QMessageBox.question(self, '提示', '开始录像，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)

    # 后摄录像提示
    def back_video_info(self):
        save_path = self.get_path(b_save_img=False, b_front=False)
        self.save_video(front=False, start=True)
        reply = QMessageBox.question(self, '提示', '开始录像，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)

    # 初始化电机
    def init_motor(self):
        reply = QMessageBox.question(self, '提示', '初始化电机成功', QMessageBox.Close, QMessageBox.Close)
        # TODO 发送初始化电机指令

    # 保存图片
    def save_img(self, front=True, save_path=None):
        """
        保存图片
        :param save_path:
        :param front:
        :return:
        """
        if front:
            cv2.imwrite(save_path, self.frame_front)
        else:
            cv2.imwrite(save_path, self.frame_back)

    # 保存视频
    def save_video(self, front=True, start=True, save_path=None):
        """
        保存视频
        :param save_path:
        :param front:是否是前置摄像头
        :param start: 是否是开始保存 True开始 False 结束保存
        :return:
        """
        # TODO 保存视频
        pass

    def show_view(self):
        m = mesh.Mesh.from_file('statics/holecube.stl')
        points = m.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        meshdata = gl.MeshData(vertexes=points, faces=faces, faceColors=[0.5, 0.5, 0.5, 0.5])
        mesh_obj = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=True, drawEdges=True,
                                 edgeColor=(1, 1, 1, 1))
        self.viewer.addItem(mesh_obj)

    def paintEvent(self, event):
        if self.open_flag:
            ret1, frame_front = self.front_video_stream.read()
            self.frame_front = frame_front
            frame_front = cv2.resize(frame_front, (640, 480), interpolation=cv2.INTER_AREA)
            frame_front = cv2.cvtColor(frame_front, cv2.COLOR_BGR2RGB)
            ret1, frame_back = self.back_video_stream.read()
            self.frame_back = frame_back
            frame_back = cv2.resize(frame_back, (150, 150), interpolation=cv2.INTER_AREA)
            frame_back = cv2.cvtColor(frame_back, cv2.COLOR_BGR2RGB)
            self.Qframe_front = QImage(frame_front.data, frame_front.shape[1], frame_front.shape[0],
                                       frame_front.shape[1] * 3, QImage.Format_RGB888)
            self.Qframe_back = QImage(frame_back.data, frame_back.shape[1], frame_back.shape[0],
                                      frame_back.shape[1] * 3, QImage.Format_RGB888)
            self.ui.front_video_label.setPixmap(QPixmap.fromImage(self.Qframe_front))
            self.ui.back_video_label.setPixmap(QPixmap.fromImage(self.Qframe_back))
            self.update()

    def keyPressEvent(self, keyevent):
        if keyevent.text() in ['w', 'W']:
            self.datamanager_obj.move = 1
        elif keyevent.text() in ['a', 'A']:
            self.datamanager_obj.move = 3
        elif keyevent.text() in ['s', 'S']:
            self.datamanager_obj.move = 2
        elif keyevent.text() in ['d', 'D']:
            self.datamanager_obj.move = 4
        elif keyevent.text() in ['q', 'Q']:
            self.datamanager_obj.move = 5
        elif keyevent.text() in ['e', 'E']:
            self.datamanager_obj.move = 6
        elif keyevent.text() in ['z', 'Z']:
            self.datamanager_obj.move = 7
        elif keyevent.text() in ['c', 'C']:
            self.datamanager_obj.move = 8
        elif keyevent.text() in ['x', 'X']:
            self.datamanager_obj.move = 0


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    main_windows = MainDialog()
    # setting_dlg = SettingWindow()
    # btn = main_windows.ui.setting_btn
    # btn.clicked.connect(setting_dlg.show)
    main_windows.show()
    sys.exit(myapp.exec_())
