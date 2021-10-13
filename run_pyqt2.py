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
from qt_material import apply_stylesheet
# from vtk import *
# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import numpy as np
from stl import mesh
import pyqtgraph.opengl as gl
import math

from dataManager import data_manager
import config
from storage import save_data


class SettingWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = setting_ui.Ui_Form()
        self.ui.setupUi(self)


class JpystickThread(QThread):
    finish = pyqtSignal(int)

    def __init__(self, parent=None, run_func=None):
        super().__init__(parent)
        self.run_func = run_func

    def run(self):
        self.run_func()


class CameraThread(QThread):
    """
    摄像头对象
    """

    def __init__(self, url, out_label, parent=None, run_func=None):
        """初始化方法"""
        super().__init__(parent)
        self.url = url
        self.outLabel = out_label
        self.run_func = run_func

    def run(self):
        self.run_func(self.url, self.outLabel)


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
        # 显示三维模型
        # self.currentSTL = None
        # self.lastDir = None
        # self.droppedFilename = None
        # self.viewer = gl.GLViewWidget()
        # self.ui.view_layout.addWidget(self.viewer, 1)
        # self.show_view()
        # 绘制角度
        # self.horizon_layout1 = QHBoxLayout()
        # self.horizon_layout2 = QHBoxLayout()
        # self.label_5 = angle.Clock_paint()
        # self.ui.horizontalLayout_3.addWidget(self.label_5)
        # self.label2 = QPushButton('Button', self)
        # self.label2.setToolTip('QPushButton')
        #
        # self.ui.x_y_latout.addWidget(self.label1)
        # self.ui.z_layout.addWidget(self.label1)
        # self.ui.x_y_z_layout.addWidget(self.label1)

        # self.ui.x_y_z_box.setLayout(self.horizon_layout1)
        # self.ui.groupBox_11.setLayout(self.horizon_layout2)
        # self.timer.timeout.connect(self.label1.update)
        # self.ui.label_5 = angle.Clock_paint()
        # self.ui.x_y_layout.addWidget(self.label1)
        # self.ui.x_y_z_box.addWidget(self.label2)
        # 设置页面
        self.setting_dlg = SettingWindow()
        # 绑定修改数据
        self.connect_single_slot()
        # 前摄后后摄图片
        self.frame_front = None
        self.frame_back = None
        # 放在线程中的人物
        # 显示视频
        self.open_flag = False
        self.front_video_work = CameraThread(url=config.front_video_src, out_label=self.ui.front_video_label,
                                             parent=None,
                                             run_func=self.display_video)
        self.front_video_work.start()
        self.back_video_work = CameraThread(url=config.back_video_src, out_label=self.ui.back_video_label, parent=None,
                                            run_func=self.display_video)
        self.back_video_work.start()
        # 获取游戏手柄数据
        self.joystick_work = JpystickThread(parent=None, run_func=self.datamanager_obj.joystick_obj.get_data)
        self.joystick_work.start()
        # 更新pid参数
        self.update_pid(value=None)
        # self.init_image()

    # 初始化背景图片
    def init_image(self):
        self.ui.init_motor_btn.setStyleSheet('QPushButton{color:#FFFFFF,border-image:url(./statics/images/装饰.png)}')
        self.ui.back_camera_cap.setStyleSheet('QPushButton{border-image:url(./statics/images/装饰.png)}')
        self.ui.back_camera_cap.setStyleSheet('QLabel{color:#FFFFFF}')
        self.ui.front_camera_cap.setStyleSheet('QPushButton{border-image:url(./statics/images/装饰.png)}')
        self.ui.front_camera_cap.setStyleSheet('QPushButton{border-image:url(./statics/images/装饰.png)}')

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

    def display_video(self, url, label):
        """显示视频 暂时不显示"""
        pass
        """
        cap = cv2.VideoCapture(url)
        start_time = time.time()
        print(cap, cap.isOpened())
        print(label.text)
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if (time.time() - start_time) > 0.1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    if url == config.front_video_src:
                        self.frame_front = frame
                        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
                    else:
                        self.frame_back = frame
                        frame = cv2.resize(frame, (150, 150), interpolation=cv2.INTER_AREA)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    start_time = time.time()
        """


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
        deep_str = "深度:%.02f m" % self.datamanager_obj.tcp_server_obj.deep
        press_str = "压力: %.02f" % self.datamanager_obj.tcp_server_obj.press
        temperature_str = "水温: %.02f" % self.datamanager_obj.tcp_server_obj.temperature
        leak_str = "未漏水 %d" % self.datamanager_obj.tcp_server_obj.is_leak_water
        speed_str = "速度 %% %d" % self.datamanager_obj.tcp_server_obj.speed
        light_str = "灯： %d" % self.datamanager_obj.tcp_server_obj.is_big_light
        sonar_str = "声呐： %d" % self.datamanager_obj.tcp_server_obj.is_sonar
        camera_steer_str = "舵机： %d" % self.datamanager_obj.tcp_server_obj.camera_angle_pwm
        arm_str = "机械臂： %d" % self.datamanager_obj.tcp_server_obj.arm_pwm
        x_angle_str = "x角度： %d" % self.datamanager_obj.tcp_server_obj.theta_list[0]
        y_angle_str = "y角度： %d" % self.datamanager_obj.tcp_server_obj.theta_list[1]
        z_angle_str = "z角度： %d" % self.datamanager_obj.tcp_server_obj.theta_list[2]
        self.ui.pressure_label.setText(press_str)
        self.ui.temperature_label.setText(temperature_str)
        self.ui.leak_label.setText(leak_str)
        self.ui.deep_label.setText(deep_str)
        self.ui.speed_label.setText(speed_str)
        self.ui.light_label.setText(light_str)
        self.ui.sonar_label.setText(sonar_str)
        self.ui.camera_steer_label.setText(camera_steer_str)
        self.ui.arm_label.setText(arm_str)
        self.ui.angle_x_label.setText(x_angle_str)
        self.ui.angle_y_label.setText(y_angle_str)
        self.ui.angle_z_label.setText(z_angle_str)
        control_info_dict = {0: ' 停止', 1: ' 前进', 2: ' 后退', 3: ' 左转', 4: ' 右转', 5: ' 上升', 6: ' 下降', 7: ' 左移',
                                  8: ' 右移'}
        mode_str = control_info_dict[self.datamanager_obj.move]
        self.ui.mode_label.setText(mode_str)

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
        return_info = self.save_img(front=True, save_path=save_path)
        if return_info is None:
            reply = QMessageBox.question(self, '提示', '截图成功，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)
        else:
            QMessageBox.question(self, '提示', return_info, QMessageBox.Close, QMessageBox.Close)

    # 后摄截图提示
    def back_cap_info(self):
        save_path = self.get_path(b_front=False)
        return_info = self.save_img(front=False, save_path=save_path)
        if return_info is None:
            reply = QMessageBox.question(self, '提示', '截图成功，路径:' + save_path, QMessageBox.Close, QMessageBox.Close)
        else:
            QMessageBox.question(self, '提示', return_info, QMessageBox.Close, QMessageBox.Close)

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
            if self.frame_front is None:
                print('前摄无数据')
                return '前摄无数据'
            else:
                cv2.imwrite(save_path, self.frame_front)
        else:
            if self.frame_back is None:
                print('后摄无数据')
                return '后摄无数据'
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

    # def paintEvent(self, event):
    #     if self.open_flag:
    #         ret1, frame_front = self.front_video_stream.read()
    #         self.frame_front = frame_front
    #         frame_front = cv2.resize(frame_front, (640, 480), interpolation=cv2.INTER_AREA)
    #         frame_front = cv2.cvtColor(frame_front, cv2.COLOR_BGR2RGB)
    #         ret1, frame_back = self.back_video_stream.read()
    #         self.frame_back = frame_back
    #         frame_back = cv2.resize(frame_back, (150, 150), interpolation=cv2.INTER_AREA)
    #         frame_back = cv2.cvtColor(frame_back, cv2.COLOR_BGR2RGB)
    #         self.Qframe_front = QImage(frame_front.data, frame_front.shape[1], frame_front.shape[0],
    #                                    frame_front.shape[1] * 3, QImage.Format_RGB888)
    #         self.Qframe_back = QImage(frame_back.data, frame_back.shape[1], frame_back.shape[0],
    #                                   frame_back.shape[1] * 3, QImage.Format_RGB888)
    #         self.ui.front_video_label.setPixmap(QPixmap.fromImage(self.Qframe_front))
    #         self.ui.back_video_label.setPixmap(QPixmap.fromImage(self.Qframe_back))
    #         self.update()
    # def textRectF(self,radius,pointsize,angle):
    #     recf = QRectF()
    #     recf.setX(radius*math.cos(angle*math.pi/180.0)-pointsize*2)
    #     recf.setY(radius*math.sin(angle*math.pi/180.0)-pointsize/2.0)
    #     recf.setWidth(pointsize*4)#宽度、高度
    #     recf.setHeight(pointsize)
    #     return recf
    #
    # def paintEvent(self, event):
    #     print('update paint')
    #     hour_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-30)]
    #     minute_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-65)]
    #     second_points = [QPoint(5,8),QPoint(-5,8),QPoint(0,-80)]
    #     hour_color = QColor(200,100,0,200)
    #     minute_color = QColor(0,127,127,150)
    #     second_color = QColor(0,160,230,150)
    #
    #     min_len = min(self.width(),self.height())
    #     time = QTime.currentTime() #获取当前时间
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.translate(self.width()/2,self.height()/2)#平移到窗口中心
    #     painter.scale(min_len/200.0,min_len/200.0) #进行尺度缩放
    #
    #     #----------绘制时针------------
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(hour_color)#颜色
    #     painter.save()
    #     # 根据 1小时时= 30°，水品方向逆时针旋转时针
    #     # painter.rotate(30.0*((time.hour()+time.minute()/60.0)))
    #     # 根据 偏航旋转角度
    #     painter.rotate(self.y)
    #     painter.drawConvexPolygon(QPolygon(hour_points))
    #     painter.restore() # save 退出，可重新设置画笔
    #
    #     painter.setPen(hour_color)
    #     #绘制小时线(360/12 = 30度)
    #     for i in range(12):
    #         painter.drawLine(88,0,96,0)#绘制水平线
    #         painter.rotate(30.0)# 原有旋转角度上进行旋转；
    #
    #     radius = 100 # 半径
    #     font = painter.font()
    #     font.setBold(True)
    #     painter.setFont(font)
    #     pointSize = font.pointSize()#字体大小
    #     # print(pointSize)
    #
    #     #绘制小时文本
    #     for i in range(12):
    #         nhour = i + 3 # 从水平 3 点进行绘制
    #         if(nhour>12):
    #             nhour -= 12
    #         painter.drawText(self.textRectF(radius*0.8,pointSize,i*30),Qt.AlignCenter,str(nhour*30))
    #
    #     #绘制分针;
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(minute_color)
    #     painter.save()
    #
    #     # 1分钟为6°，
    #     # painter.rotate(6.0*(time.minute()+time.second()/60.0))
    #     painter.rotate(self.p)
    #     painter.drawConvexPolygon(QPolygon(minute_points))
    #     painter.restore()
    #
    #     #绘制分针线
    #     painter.setPen(minute_color)
    #     for i in range(60):
    #         if(i%5 !=0):
    #             painter.drawLine(92,0,96,0)
    #         painter.rotate(6.0)
    #
    #     #绘制秒针
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(second_color)
    #     painter.save()
    #     #绘制秒线
    #     # painter.rotate(6.0*time.second())
    #     painter.rotate(self.r)
    #     painter.drawConvexPolygon(QPolygon(second_points))
    #     painter.restore()
    #
    #     painter.setPen(second_color)
    #     for i in range(360):
    #         if(i%5!=0 or i%30!=0):#绘制
    #             painter.drawLine(94,0,96,0)
    #         painter.rotate(1.0)#旋转


    def keyPressEvent(self, keyevent):
        if keyevent.text() in ['w', 'W']:
            self.datamanager_obj.move = 1
        elif keyevent.text() in ['a', 'A']:
            self.datamanager_obj.move = 3
        elif keyevent.text() in ['s', 'S']:
            self.datamanager_obj.move = 2
        elif keyevent.text() in ['d', 'D']:
            self.datamanager_obj.move = 4
        elif keyevent.text() in ['z', 'Z']:
            self.datamanager_obj.move = 5
        elif keyevent.text() in ['c', 'C']:
            self.datamanager_obj.move = 6
        elif keyevent.text() in ['q', 'Q']:
            self.datamanager_obj.move = 7
        elif keyevent.text() in ['e', 'E']:
            self.datamanager_obj.move = 8
        elif keyevent.text() in ['x', 'X']:
            self.datamanager_obj.move = 0


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    main_windows = MainDialog()
    main_windows.resize(1920,1080)
    # main_windows.setStyleSheet("#MainWindow{border-image:url(./statics/images/背景.png);}")  # 设置背景图
    # setting_dlg = SettingWindow()
    # btn = main_windows.ui.setting_btn
    # btn.clicked.connect(setting_dlg.show)
    apply_stylesheet(myapp, theme='dark_teal.xml')
    main_windows.show()
    sys.exit(myapp.exec_())
