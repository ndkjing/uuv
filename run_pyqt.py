# coding:utf-8
import copy
import sys
import os
import time

import pyqtgraph

from ui import main_ui, setting_ui, angle
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import PyQt5
import cv2
from PIL import ImageFont, ImageDraw, Image
# from qt_material import apply_stylesheet
import numpy as np
import math

from dataManager import data_manager
from common import draw_angle
import config
from storage import save_data
import resource


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


class SonarThread(QThread):
    def __init__(self, parent=None, run_func=None, run_path=None):
        super().__init__(parent)
        self.run_path = run_path
        self.run_func = run_func

    def run(self):
        os.system(self.run_path)


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


class CameraThreadSignal(QThread):
    changePixmap = pyqtSignal(QImage)
    width = 1350
    height = 750

    def __init__(self, parent=None, run_func=None):
        super().__init__(parent)
        self.run_func = run_func

    def run(self):
        self.run_func()


class CameraThreadSignalBack(QThread):
    changePixmap = pyqtSignal(QImage)
    width = 300
    height = 100

    def __init__(self, parent=None, run_func=None):
        super().__init__(parent)
        self.run_func = run_func

    def run(self):
        self.run_func()


# 检验是否包含中文字符
def is_contain_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


class SaveVideoThread(QThread):
    """
    保存视频类
    """

    def __init__(self, front=True, save_path=None, parent=None, run_func=None):
        """初始化方法"""
        super().__init__(parent)
        self.front = front
        self.save_path = save_path
        self.run_func = run_func

    def run(self):
        self.run_func(self.front, self.save_path)


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        # self.isPressed = False
        # # 背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # # 无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        # # 鼠标跟踪
        # self.setMouseTracking(True)
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.datamanager_obj = data_manager.DataManager()
        self.draw_angle_obj = draw_angle.DrawAngle(20, 225)
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_data)
        self.timer.timeout.connect(self.update_base_info)
        self.timer.start(100)
        self.timer1 = QTimer()  # 定时器
        self.timer1.timeout.connect(self.update)
        self.timer1.timeout.connect(self.paint_angle)  # 更新角度
        self.timer1.start(1000)  # 每1s 更新一次
        self.sonar_obj = SonarThread(parent=None, run_func=self.open_sonar)
        # 写入视频
        self.is_write_frame_front = False  # 当前写入视频标志位
        self.write_frame_front_show_msg = ""  # 保存视频提示字符串成功提示路径 失败提示失败
        self.is_write_frame_back = False  # 当前写入视频标志位
        self.write_frame_back_show_msg = ""  # 保存视频提示字符串成功提示路径 失败提示失败
        # 设置页面
        self.setting_dlg = SettingWindow()
        # 绑定修改数据
        self.connect_single_slot()
        # 前摄后后摄图片
        self.frame_front = None
        self.frame_back = None
        # 视频上显示字符字典
        self.frame_text_dict = {'text1': [], 'text2': [], 'text3': []}
        # 放在线程中的人物
        # 显示视频
        self.open_flag = False
        # self.front_video_work = CameraThread(url=config.front_video_src, out_label=self.ui.front_video_label,
        #                                      parent=None,
        #                                      run_func=self.display_front_video)
        #
        # self.back_video_work = CameraThread(url=config.back_video_src, out_label=self.ui.back_video_label, parent=None,
        #                                     run_func=self.display_back_video)
        self.front_video_work = CameraThreadSignal(parent=None, run_func=self.show_front_video)
        self.front_video_work.changePixmap.connect(self.set_image)
        self.front_video_work.start()
        time.sleep(0.02)
        self.back_video_work = CameraThreadSignalBack(parent=None, run_func=self.show_back_video)
        self.back_video_work.changePixmap.connect(self.set_image_back)
        self.back_video_work.start()
        # 保存视频
        self.save_front_video_work = SaveVideoThread(front=True, save_path=None,
                                                     parent=None,
                                                     run_func=self.save_video)
        self.save_back_video_work = SaveVideoThread(front=False, save_path=None,
                                                    parent=None,
                                                    run_func=self.save_video)
        # 获取游戏手柄数据
        self.joystick_work = JpystickThread(parent=None, run_func=self.datamanager_obj.joystick_obj.thread_joystick)
        self.joystick_work.start()
        # 更新pid参数
        self.update_pid(value=None)
        self.init_base_ui()
        self.front_video_position = 0  # 前摄视频流位置  0：在中间   1在后摄位置

    def show_front_video(self):
        while True:
            cap = cv2.VideoCapture(config.front_video_src)
            if not cap.isOpened():
                time.sleep(1)
                continue
            start_time = time.time()
            last_read_time = None
            while True:
                ret, frame = cap.read()
                # print(time.time(),'ret',ret)
                if ret:
                    if (time.time() - start_time) > 0.1:
                        # 绘制文字
                        w_frame = 1350
                        h_frame = 750
                        for k, v in self.frame_text_dict.items():
                            if len(v) == 3:
                                if v[0] == 0:
                                    w = 20
                                elif v[0] == 1:
                                    w = int(w_frame / 2)
                                else:
                                    w = w_frame - 20*len(v[2])
                                if v[1] == 0:
                                    h = 100
                                elif v[1] == 1:
                                    h = int(h_frame / 2)
                                else:
                                    h = h_frame - 20*len(v[2])
                                # 判断是否包含中文
                                if is_contain_chinese(v[2]):
                                    fontpath = "./simsun.ttc"  # <== 这里是宋体字体路径
                                    font = ImageFont.truetype(fontpath, 40)  # 32为字体大小
                                    img_pil = Image.fromarray(frame)
                                    draw = ImageDraw.Draw(img_pil)
                                    draw.text((w, h), v[2], font=font, fill=(100, 1, 1, 1))
                                    frame = np.array(img_pil)
                                else:
                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    cv2.putText(frame, v[2], (w, h), font, 2, (0, 0, 155), 1, cv2.LINE_AA)
                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        self.frame_front = rgbImage
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                        # p = convertToQtFormat.scaled(1350, 750, Qt.KeepAspectRatio)
                        p = convertToQtFormat.scaled(self.ui.front_video_label.width(),
                                                     self.ui.front_video_label.height(), Qt.KeepAspectRatio)
                        # print('front_video_label', self.ui.front_video_label.size())
                        # print('back_video_label', self.ui.back_video_label.size())
                        self.front_video_work.changePixmap.emit(p)
                        start_time = time.time()
                else:
                    cap.release()
                    break

    def show_back_video(self):
        while True:
            cap = cv2.VideoCapture(config.back_video_src)
            if not cap.isOpened():
                time.sleep(1)
                continue
            start_time = time.time()
            while True:
                ret, frame = cap.read()
                # print(time.time(),'ret',ret)
                if ret:
                    if (time.time() - start_time) > 0.13:
                        # 绘制文字
                        w_frame = 300
                        h_frame = 100
                        for k, v in self.frame_text_dict.items():
                            if len(v) == 3:
                                if v[0] == 0:
                                    w = 100
                                elif v[0] == 1:
                                    w = int(w_frame / 2)
                                else:
                                    w = w_frame - 200
                                if v[1] == 0:
                                    h = 100
                                elif v[1] == 1:
                                    h = int(h_frame / 2)
                                else:
                                    h = h_frame - 200
                                # 判断是否包含中文
                                if is_contain_chinese(v[2]):
                                    fontpath = "./simsun.ttc"  # <== 这里是宋体字体路径
                                    font = ImageFont.truetype(fontpath, 40)  # 32为字体大小
                                    img_pil = Image.fromarray(frame)
                                    draw = ImageDraw.Draw(img_pil)
                                    draw.text((w, h), v[2], font=font, fill=(100, 1, 1, 1))
                                    frame = np.array(img_pil)
                                else:
                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    cv2.putText(frame, v[2], (w, h), font, 2, (0, 0, 155), 1, cv2.LINE_AA)
                        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        self.frame_back = rgbImage
                        h, w, ch = rgbImage.shape
                        bytesPerLine = ch * w
                        convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                        # p = convertToQtFormat.scaled(400, 200, Qt.KeepAspectRatio)
                        p = convertToQtFormat.scaled(self.ui.back_video_label.width(), self.ui.back_video_label.width(),
                                                     Qt.KeepAspectRatio)
                        self.back_video_work.changePixmap.emit(p)
                        start_time = time.time()
                else:
                    cap.release()
                    break

    @pyqtSlot(QImage)
    def set_image(self, image):
        time1 = time.time()
        pix_image = QPixmap.fromImage(image)
        time2 = time.time()
        # piximage 转为array
        # qimg = pix_image.toImage()
        # temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        # temp_shape += (4,)
        # ptr = qimg.bits()
        # ptr.setsize(qimg.byteCount())
        # result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        # result = result[..., :3]
        # self.frame_front = result
        # print(self.ui.front_video_label.width(), self.ui.front_video_label.height())
        if self.front_video_position == 0:
            self.ui.front_video_label.setPixmap(pix_image)
        else:
            self.ui.back_video_label.setPixmap(pix_image)
        time3 = time.time()
        # print("change time",time3-time2,"show_time",time2-time1)

    @pyqtSlot(QImage)
    def set_image_back(self, image):
        pix_image = QPixmap.fromImage(image)
        # qimg = pix_image.toImage()
        # temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        # temp_shape += (4,)
        # ptr = qimg.bits()
        # ptr.setsize(qimg.byteCount())
        # result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        # result = result[..., :3]
        # self.frame_back = result
        if self.front_video_position == 0:
            self.ui.back_video_label.setPixmap(pix_image)
        else:
            self.ui.front_video_label.setPixmap(pix_image)

    # 绘制角度
    def paint_angle(self):
        """
        绘制陀螺仪角度
        :return:
        """
        # self.ui.angle_x_label.setScaledContents(True)
        self.draw_angle_obj.draw_y(self.datamanager_obj.tcp_server_obj.theta_list[1])
        self.draw_angle_obj.draw_z(self.datamanager_obj.tcp_server_obj.theta_list[2])
        if os.path.exists(config.save_angle_y_path):
            pix_y = QPixmap(config.save_angle_y_path)
            self.ui.angle_y_label.setPixmap(pix_y)
        if os.path.exists(config.save_angle_z_path):
            pix_z = QPixmap(config.save_angle_z_path)
            self.ui.angle_z_label.setPixmap(pix_z)
        # 下面方式不行 暂时没弄懂为什么
        # self.horizon_layout2 = QHBoxLayout()
        # self.label_5 = angle.Clock_paint()
        # self.ui.horizontalLayout_3.addWidget(self.label_5)

    # 初始化UI
    def init_base_ui(self):
        """
        初始化UI和设置一些UI启动值
        :return:
        """
        self.setWindowTitle('行星轮水下机器人')
        self.setWindowIcon(QIcon(':/icons/uuvImages/logo.png'))
        # self.setWindowIcon(QIcon('uuvImages/logo.png'))
        # 滑动条最大值在左边，所以这样设置
        # 设置字体大小
        self.ui.switch_video_label.setFont(QFont('Arial', 16))
        self.ui.switch_video_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.setting_label.setFont(QFont('Arial', 16))
        self.ui.setting_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.back_label.setFont(QFont('Arial', 16))
        self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.front_label.setFont(QFont('Arial', 16))
        self.ui.front_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.logo_label.setFont(QFont('Arial', 18,QFont.Bold))
        self.ui.logo_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.leak_label.setFont(QFont('Arial', 16))
        self.ui.leak_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.arm_label.setFont(QFont('Arial', 16))
        self.ui.arm_label.setStyleSheet("color:rgb(255,255,255,255)")
        # self.ui.front_video_label.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.front_camera_cap.setFont(QFont('Arial', 16))
        self.ui.front_camera_cap.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.front_camera_video.setFont(QFont('Arial', 16))
        self.ui.front_camera_video.setStyleSheet("color:rgb(255,255,255,255)")
        # self.ui.back_video_label.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.back_camera_cap.setFont(QFont('Arial', 16))
        self.ui.back_camera_cap.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.back_camera_video.setFont(QFont('Arial', 16))
        self.ui.back_camera_video.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.mode_label.setFont(QFont('Arial', 16))
        self.ui.mode_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.deep_label.setFont(QFont('Arial', 16))
        self.ui.deep_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.temperature_label.setFont(QFont('Arial', 16))
        self.ui.temperature_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.switch_video_button.setFont(QFont('Arial', 16))
        # self.ui.switch_video_button.setStyleSheet("color:rgb(255,255,255,255)")
        # self.ui.open_sonar_btn.setFont(QFont('Arial', 16))
        self.ui.setting_btn.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.headlight_label.setFont(QFont('Arial', 16))
        self.ui.headlight_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.led_label.setFont(QFont('Arial', 16))
        self.ui.led_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.steer_label.setFont(QFont('Arial', 16))
        self.ui.steer_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.press_label.setFont(QFont('Arial', 16))
        self.ui.press_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.speed_label.setFont(QFont('Arial', 16))
        self.ui.speed_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.robot_text_label.setFont(QFont('Arial', 16))
        self.ui.robot_text_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.joystick_text_label.setFont(QFont('Arial', 16))
        self.ui.joystick_text_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.auto_label.setFont(QFont('Arial',20, 16))
        self.ui.auto_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.auto_deep_label.setFont(QFont('Arial', 16))
        self.ui.auto_deep_label.setStyleSheet("color:rgb(193,113,4,255)")
        self.ui.auto_direction_label.setFont(QFont('Arial', 16))
        self.ui.auto_direction_label.setStyleSheet("color:rgb(193,113,4,255)")
        self.ui.keep_deep_btn.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.keep_direction_btn.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.move_deep_btn.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.move_direction_btn.setFont(QFont('Arial', 16))
        # self.ui.back_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.v_label.setFont(QFont('Arial', 16))
        self.ui.v_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.sonar_text_label.setFont(QFont('Arial', 16))
        self.ui.sonar_text_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.direct_x_label.setFont(QFont('Arial', 16))
        self.ui.direct_x_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.direct_y_label.setFont(QFont('Arial', 16))
        self.ui.direct_y_label.setStyleSheet("color:rgb(255,255,255,255)")
        self.ui.direct_z_label.setFont(QFont('Arial', 16))
        self.ui.direct_z_label.setStyleSheet("color:rgb(255,255,255,255)")
        # 设置按钮为按下不弹起
        self.ui.front_camera_video.setCheckable(True)
        self.ui.back_camera_video.setCheckable(True)
        # 设置当前显示视频地址
        self.setting_dlg.ui.fva_line_edit.setText(str(config.front_video_src))
        self.setting_dlg.ui.bva_line_edit.setText(str(config.back_video_src))
        # 摄像头图标设置
        self.ui.front_camera_cap.setText('')
        self.ui.front_camera_cap.setFixedWidth(32)
        self.ui.front_camera_cap.setFixedHeight(32)
        self.ui.front_camera_cap.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/拍照.png)}")
        self.ui.front_camera_video.setText('')
        self.ui.front_camera_video.setFixedWidth(32)
        self.ui.front_camera_video.setFixedHeight(32)
        self.ui.front_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
        self.ui.back_camera_cap.setText('')
        self.ui.back_camera_cap.setFixedWidth(32)
        self.ui.back_camera_cap.setFixedHeight(32)
        self.ui.back_camera_cap.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/拍照.png)}")
        self.ui.back_camera_video.setText('')
        self.ui.back_camera_video.setFixedWidth(32)
        self.ui.back_camera_video.setFixedHeight(32)
        self.ui.back_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
        # 设置背景图片
        self.ui.robot_img_btn.setFixedWidth(22)
        self.ui.robot_img_btn.setFixedHeight(22)
        self.ui.robot_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/不在线.png)}")
        self.ui.joystick_img_btn.setFixedWidth(22)
        self.ui.joystick_img_btn.setFixedHeight(22)
        self.ui.joystick_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/不在线.png)}")
        self.ui.headlight_img_btn.setFixedWidth(22)
        self.ui.headlight_img_btn.setFixedHeight(22)
        self.ui.headlight_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
        self.ui.led_img_btn.setFixedWidth(22)
        self.ui.led_img_btn.setFixedHeight(22)
        self.ui.led_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
        self.ui.arm_img_btn.setFixedWidth(22)
        self.ui.arm_img_btn.setFixedHeight(22)
        self.ui.arm_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
        self.ui.steer_img_btn.setFixedWidth(22)
        self.ui.steer_img_btn.setFixedHeight(22)
        self.ui.steer_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/云台停止.png)}")
        self.ui.steer_img_btn.setFixedWidth(22)
        self.ui.steer_img_btn.setFixedHeight(22)
        self.ui.steer_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/前进.png)}")
        self.ui.open_sonar_btn.setText('')
        self.ui.open_sonar_btn.setFixedWidth(22)
        self.ui.open_sonar_btn.setFixedHeight(22)
        self.ui.open_sonar_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
        self.ui.switch_video_button.setText('')
        self.ui.switch_video_button.setFixedWidth(22)
        self.ui.switch_video_button.setFixedHeight(22)
        self.ui.switch_video_button.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/切换.png)}")
        self.ui.setting_btn.setText('')
        self.ui.setting_btn.setFixedWidth(22)
        self.ui.setting_btn.setFixedHeight(22)
        self.ui.setting_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/设置.png)}")
        self.ui.mode_img_btn.setFixedWidth(22)
        self.ui.mode_img_btn.setFixedHeight(22)
        self.ui.mode_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/停止.png)}")
        # self.ui.groupBox_3.setFixedWidth(1800)
        # self.ui.groupBox_3.setFixedHeight(626)
        # 设置边框线
        self.ui.front_video_label.setFixedWidth(1346)
        self.ui.front_video_label.setFixedHeight(842)
        # 设置边框样式 可选样式有Box Panel等
        self.ui.front_video_label.setFrameShape(QFrame.Box)
        # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        # self.ui.front_video_label.setFrameShadow(QFrame.Raised)
        # 设置线条宽度
        self.ui.front_video_label.setLineWidth(5)
        # 设置背景颜色，包括边框颜色
        self.ui.front_video_label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')
        print(self.ui.front_video_label.width(), self.ui.front_video_label.height())
        self.ui.front_video_label.setScaledContents(True)  # 设置图片自动适应标签大小
        self.ui.back_video_label.setFixedWidth(446)
        self.ui.back_video_label.setFixedHeight(223)
        # 设置边框样式 可选样式有Box Panel等
        self.ui.back_video_label.setFrameShape(QFrame.Box)
        # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.ui.back_video_label.setFrameShadow(QFrame.Raised)
        # 设置线条宽度
        self.ui.back_video_label.setLineWidth(5)
        # 设置背景颜色，包括边框颜色
        self.ui.back_video_label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')
        self.ui.back_video_label.setScaledContents(True)  # 设置图片自动适应标签大小

    # 初始化背景图片
    def init_image(self):
        # self.ui.init_motor_btn.setStyleSheet('QPushButton{color:#FFFFFF,border-image:url(./statics/images/装饰.png)}')
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
        # 视频地址设置绑定
        # 视频添加文字水印绑定
        self.setting_dlg.ui.text1_button.clicked.connect(self.update_frame_text)
        self.setting_dlg.ui.text2_button.clicked.connect(self.update_frame_text)
        self.setting_dlg.ui.text3_button.clicked.connect(self.update_frame_text)
        self.setting_dlg.ui.fva_button.clicked.connect(self.update_video_address)
        self.setting_dlg.ui.bva_button.clicked.connect(self.update_video_address)
        # 打开声呐
        self.ui.open_sonar_btn.clicked.connect(self.open_sonar)
        # 定向和定深
        self.ui.keep_direction_btn.clicked.connect(self.deep_direction)
        self.ui.move_direction_btn.clicked.connect(self.deep_direction)
        self.ui.keep_deep_btn.clicked.connect(self.deep_direction)
        self.ui.move_deep_btn.clicked.connect(self.deep_direction)
        self.ui.switch_video_button.clicked.connect(self.change_front_video_position)

    # 更新视频位置回调函数
    def change_front_video_position(self):
        if self.front_video_position == 0:
            self.front_video_position = 1
        elif self.front_video_position == 1:
            self.front_video_position = 0

    # 朝向和深度保持
    def deep_direction(self):
        if self.sender() == self.ui.keep_direction_btn and self.ui.move_direction_btn.isChecked():
            self.ui.move_direction_btn.setChecked(False)
        if self.sender() == self.ui.move_direction_btn and self.ui.keep_direction_btn.isChecked():
            self.ui.keep_direction_btn.setChecked(False)
        if self.sender() == self.ui.move_deep_btn and self.ui.keep_deep_btn.isChecked():
            self.ui.keep_deep_btn.setChecked(False)
        if self.sender() == self.ui.keep_deep_btn and self.ui.move_deep_btn.isChecked():
            self.ui.move_deep_btn.setChecked(False)
        if self.ui.keep_direction_btn.isChecked():
            self.datamanager_obj.b_keep_direction = 1
        else:
            self.datamanager_obj.b_keep_direction = 0

        if self.ui.move_direction_btn.isChecked():
            self.datamanager_obj.b_move_direction = 1
        else:
            self.datamanager_obj.b_move_direction = 0
        if self.ui.keep_deep_btn.isChecked():
            self.datamanager_obj.b_keep_deep = 1
        else:
            self.datamanager_obj.b_keep_deep = 0
        if self.ui.move_deep_btn.isChecked():
            self.datamanager_obj.b_move_deep = 1
        else:
            self.datamanager_obj.b_move_deep = 0

    # 打开声呐
    def open_sonar(self):
        if self.datamanager_obj.sonar:
            self.datamanager_obj.sonar = 0
        else:
            self.datamanager_obj.sonar = 1
        print('open sonar')
        # import subprocess
        command_sonar1 = "F:\\apps\pingviewer_release\deploy\pingviewer.exe"
        command_sonar2 = "D:\\apps\pingviewer_release\deploy\pingviewer.exe"
        command_sonar3 = "F:\pingviewer_release\deploy\pingviewer.exe"
        command_sonar4 = "D:\pingviewer_release\deploy\pingviewer.exe"
        if os.path.exists(command_sonar1):
            self.sonar_obj.run_path = command_sonar1
            self.sonar_obj.start()
            # rc, out = subprocess.getstatusoutput(command_sonar1)
        elif os.path.exists(command_sonar2):
            self.sonar_obj.run_path = command_sonar2
            self.sonar_obj.start()
        elif os.path.exists(command_sonar3):
            self.sonar_obj.run_path = command_sonar3
            self.sonar_obj.start()
        elif os.path.exists(command_sonar4):
            self.sonar_obj.run_path = command_sonar4
            self.sonar_obj.start()
            # subprocess.getstatusoutput(command_sonar4)
            # r_v = os.system(command_sonar4)

    def start_video(self):
        print('start video')
        self.front_video_work.start()
        # self.back_video_work.start()

    def update_video_address(self):
        if self.sender() == self.setting_dlg.ui.fva_button:
            print('fva_line_edit', self.setting_dlg.ui.fva_line_edit.text())
            if self.setting_dlg.ui.fva_line_edit.text() != config.front_video_src:
                print('update fva')
                self.front_video_work.url = self.setting_dlg.ui.fva_line_edit.text()
                config.front_video_src = self.setting_dlg.ui.fva_line_edit.text()
        if self.sender() == self.setting_dlg.ui.bva_button:
            print('bva_line_edit', self.setting_dlg.ui.bva_line_edit.text())
            if self.setting_dlg.ui.bva_line_edit.text() != config.back_video_src:
                config.back_video_src = self.setting_dlg.ui.bva_line_edit.text()
                print('update bva')

    # 更新视频文字水印
    def update_frame_text(self):
        if self.sender() == self.setting_dlg.ui.text1_button:
            show_text1 = self.setting_dlg.ui.text1_line_edit.text()
            t1_x = self.setting_dlg.ui.text1_x_combo_box.currentIndex()
            t1_y = self.setting_dlg.ui.text1_y_combo_box.currentIndex()
            if show_text1:
                self.frame_text_dict['text1'] = [t1_x, t1_y, show_text1]
            else:
                self.frame_text_dict['text1'] = []
        elif self.sender() == self.setting_dlg.ui.text2_button:
            show_text2 = self.setting_dlg.ui.text2_line_edit.text()
            t2_x = self.setting_dlg.ui.text2_x_combo_box.currentIndex()
            t2_y = self.setting_dlg.ui.text2_y_combo_box.currentIndex()
            if show_text2:
                self.frame_text_dict['text2'] = [t2_x, t2_y, show_text2]
            else:
                self.frame_text_dict['text2'] = []
        elif self.sender() == self.setting_dlg.ui.text3_button:
            show_text3 = self.setting_dlg.ui.text3_line_edit.text()
            t3_x = self.setting_dlg.ui.text3_x_combo_box.currentIndex()
            t3_y = self.setting_dlg.ui.text3_y_combo_box.currentIndex()
            if show_text3:
                self.frame_text_dict['text3'] = [t3_x, t3_y, show_text3]
            else:
                self.frame_text_dict['text3'] = []

    # 更新pid参数
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

    # 更新设置数据
    def update_setting_data(self):
        self.setting_dlg.ui.ip_address_label.setText(str(self.datamanager_obj.tcp_server_obj.bind_ip + \
                                                         ':' + str(self.datamanager_obj.tcp_server_obj.bind_port)))

        self.setting_dlg.ui.joystick_label.setText('遥控:' + str(self.datamanager_obj.joystick_obj.joy_obj.count))

    def start_server(self):
        self.setting_dlg.ui.ip_address_line_edit.setText(str(self.datamanager_obj.tcp_server_obj.bind_ip))
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

    def display_front_video(self, url, label):
        """显示前置摄像头视频"""
        while True:
            if not self.ui.show_video_button.isChecked():
                time.sleep(1)
                continue
            else:
                break
        while True:
            print('url', url)
            cap = cv2.VideoCapture(url)
            print('cap info', cap, cap.isOpened())
            start_time = time.time()
            while cap.isOpened():
                success, frame = cap.read()
                # print(time.time(), success, type(frame))
                if success:
                    if (time.time() - start_time) > 0.1:
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        # 绘制文字
                        for k, v in self.frame_text_dict.items():
                            if len(v) == 3:
                                if v[0] == 0:
                                    w = 100
                                elif v[0] == 1:
                                    w = int(frame.shape[1] / 2)
                                else:
                                    w = frame.shape[1] - 200
                                if v[1] == 0:
                                    h = 100
                                elif v[1] == 1:
                                    h = int(frame.shape[0] / 2)
                                else:
                                    h = frame.shape[0] - 200
                                # 判断是否包含中文
                                if is_contain_chinese(v[2]):
                                    fontpath = "./simsun.ttc"  # <== 这里是宋体字体路径
                                    font = ImageFont.truetype(fontpath, 40)  # 32为字体大小
                                    img_pil = Image.fromarray(frame)
                                    draw = ImageDraw.Draw(img_pil)
                                    draw.text((w, h), v[2], font=font, fill=(100, 1, 1, 1))
                                    frame = np.array(img_pil)
                                else:
                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    cv2.putText(frame, v[2], (w, h), font, 2, (0, 0, 155), 1, cv2.LINE_AA)
                        self.frame_front = frame
                        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
                        # print(time.time(), 'front width height', self.ui.front_video_label.width(),
                        #       self.ui.front_video_label.height())
                        frame = cv2.resize(frame,
                                           (self.ui.front_video_label.width(), self.ui.front_video_label.height()),
                                           interpolation=cv2.INTER_AREA)
                        img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                        pix_img = QPixmap.fromImage(img)
                        # print(time.time())
                        label.setPixmap(pix_img)
                        cv2.waitKey(1)
                        # try:
                        #     label.setPixmap()
                        # except Exception as e:
                        #     print('set video error', e)
                        # self.update()
                        start_time = time.time()
                    else:
                        time.sleep(0.03)
                        # cv2.waitKey(40)
                else:
                    break
            print('cap cloase')
            cap.release()

    def display_back_video(self, url, label):
        """显示后置摄像头视频视频"""
        while True:
            if not self.ui.show_video_button.isChecked():
                time.sleep(1)
                continue
            else:
                break
        cap = cv2.VideoCapture(url)
        print('url', url)
        start_time = time.time()
        print(cap, cap.isOpened())
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if (time.time() - start_time) > 0.1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    # 绘制文字
                    for k, v in self.frame_text_dict.items():
                        if len(v) == 3:
                            if v[0] == 0:
                                w = 100
                            elif v[0] == 1:
                                w = int(frame.shape[1] / 2)
                            else:
                                w = frame.shape[1] - 200
                            if v[1] == 0:
                                h = 100
                            elif v[1] == 1:
                                h = int(frame.shape[0] / 2)
                            else:
                                h = frame.shape[0] - 200
                            # 判断是否包含中文
                            if is_contain_chinese(v[2]):
                                fontpath = "./simsun.ttc"  # <== 这里是宋体字体路径  存在放jing_vision/utils下
                                font = ImageFont.truetype(fontpath, 40)  # 32为字体大小
                                img_pil = Image.fromarray(frame)
                                draw = ImageDraw.Draw(img_pil)
                                draw.text((w, h), v[2], font=font, fill=(100, 1, 1, 1))
                                frame = np.array(img_pil)
                            else:
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                cv2.putText(frame, v[2], (w, h), font, 2, (200, 255, 155), 1, cv2.LINE_AA)
                    print(time.time(), 'back width height', self.ui.front_video_label.width(),
                          self.ui.front_video_label.height())
                    self.frame_back = frame
                    frame = cv2.resize(frame, (self.ui.back_video_label.width(), self.ui.back_video_label.height()),
                                       interpolation=cv2.INTER_AREA)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    try:
                        label.setPixmap(QPixmap.fromImage(img))
                    except Exception as e:
                        print('set video error', e)
                    # cv2.waitKey(1)
                    self.update()
                    start_time = time.time()

    # 发送数据
    def send_data(self):
        if self.datamanager_obj.tcp_server_obj.b_connect:
            self.datamanager_obj.send_tcp_data(b_once=True)
        # 测试显示数据
        # print('front_video_label', self.ui.front_video_label.size())
        # print('back_video_label', self.ui.back_video_label.size())

    # 显示数据
    def update_base_info(self):
        if self.datamanager_obj.tcp_server_obj.b_connect == 1:
            self.ui.robot_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/在线.png)}")
        else:
            self.ui.robot_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/不在线.png)}")
        if self.datamanager_obj.joystick_obj.joy_obj.b_connect == 1:
            self.ui.joystick_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/在线.png)}")
        else:
            self.ui.joystick_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/不在线.png)}")
        deep_str = " 深度:%.02f m" % self.datamanager_obj.tcp_server_obj.deep
        press_str = " 压力: %.02f " % self.datamanager_obj.tcp_server_obj.press
        temperature_str = " 水温: %.02f " % self.datamanager_obj.tcp_server_obj.temperature
        if self.datamanager_obj.tcp_server_obj.is_leak_water < 1000:
            leak_str = " 未漏水(%d) " % self.datamanager_obj.tcp_server_obj.is_leak_water
        else:
            leak_str = " *已漏水(%d)* " % self.datamanager_obj.tcp_server_obj.is_leak_water
        speed_str = " 速度  % d %% " % (self.datamanager_obj.tcp_server_obj.speed * 25)
        if self.datamanager_obj.joystick_obj.joy_obj.b_headlight:
            light_str = " 灯： 开 "
            self.ui.headlight_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/开.png)}")
        else:
            self.ui.headlight_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
            light_str = " 灯： 关 "
        if self.datamanager_obj.joystick_obj.joy_obj.b_ledlight:
            light_str = " 灯： 开 "
            self.ui.led_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/开.png)}")
        else:
            self.ui.led_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
            light_str = " 灯： 关 "
        if self.datamanager_obj.tcp_server_obj.is_sonar:
            sonar_str = " 开 "
            self.ui.open_sonar_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/开.png)}")
        else:
            sonar_str = " 关 "
            self.ui.open_sonar_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/关.png)}")
        if self.datamanager_obj.tcp_server_obj.camera_angle_pwm == 0:
            camera_steer_str = "停止"
        elif self.datamanager_obj.tcp_server_obj.camera_angle_pwm == 2:
            camera_steer_str = "云台上"
        else:
            camera_steer_str = "云台下"
        self.ui.steer_img_btn.setStyleSheet(
            "QPushButton{border-image: url(:/icons/uuvImages/%s.png)}" % camera_steer_str)
        if self.datamanager_obj.tcp_server_obj.arm_pwm == 0:
            arm_str = "关"
        elif self.datamanager_obj.tcp_server_obj.arm_pwm == 1:
            arm_str = "开"
        else:
            arm_str = "关"
        self.ui.arm_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/%s.png)}" % arm_str)
        x_angle_str = " 俯仰角： %d " % self.datamanager_obj.tcp_server_obj.theta_list[0]
        y_angle_str = " 横滚角： %d " % self.datamanager_obj.tcp_server_obj.theta_list[1]
        z_angle_str = " 偏航角： %d " % self.datamanager_obj.tcp_server_obj.theta_list[2]
        self.ui.direct_x_label.setText(z_angle_str)
        self.ui.direct_y_label.setText(x_angle_str)
        self.ui.direct_z_label.setText(y_angle_str)
        self.ui.press_label.setText(press_str)
        self.ui.temperature_label.setText(temperature_str)
        self.ui.leak_label.setText(leak_str)
        self.ui.deep_label.setText(deep_str)
        self.ui.speed_label.setText(speed_str)
        # 直接字符显示角度
        # self.ui.angle_x_label.setText(x_angle_str)
        # self.ui.angle_y_label.setText(y_angle_str)
        # self.ui.angle_z_label.setText(z_angle_str)
        # 设置运动模式提示停止
        control_info_dict = {0: '停止', 1: '前进', 2: '后退', 3: '左转', 4: '右转', 5: '上升', 6: '下降', 7: '左移',
                             8: '右移'}
        mode_str = control_info_dict[self.datamanager_obj.tcp_server_obj.move]
        self.ui.mode_img_btn.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/%s.png)}" % mode_str)
        self.ui.auto_deep_label.setText(" 深度: %f " % 1)
        self.ui.auto_direction_label.setText(" 航向: %f" % 1)

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
                save_path = os.path.join(config.save_videos_dir, str_time + 'front_.avi')
            else:
                save_path = os.path.join(config.save_videos_dir, str_time + 'back_.avi')
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
        # 开始录像
        if self.ui.front_camera_video.isChecked():
            save_path = self.get_path(b_save_img=False)
            self.save_front_video_work.save_path = save_path
            self.is_write_frame_front = True
            # 启动保存线程
            self.save_front_video_work.start()
            # 如果保存失败则设置按钮为弹起，并提示用户
            time.sleep(0.2)  # 等待线程中先更新数据
            if self.write_frame_front_show_msg:
                show_msg = self.write_frame_front_show_msg
                self.ui.front_camera_video.setChecked(False)
                self.write_frame_front_show_msg = ''
                self.ui.front_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
            else:
                # 切换图片
                self.ui.front_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像开始.png)}")
                show_msg = '开始录像，路径:' + save_path
        # 结束录像
        else:
            print('self.ui.front_camera_video.isChecked()', self.ui.front_camera_video.isChecked())
            self.ui.front_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
            self.is_write_frame_front = False
            self.write_frame_front_show_msg = ''
            show_msg = '结束录制'
        reply = QMessageBox.question(self, '提示', show_msg, QMessageBox.Close, QMessageBox.Close)

    # 后摄录像提示
    def back_video_info(self):
        # 开始录像
        if self.ui.back_camera_video.isChecked():
            save_path = self.get_path(b_save_img=False, b_front=False)
            self.save_back_video_work.save_path = save_path
            self.is_write_frame_back = True
            self.save_back_video_work.start()
            # 如果保存失败则设置按钮为弹起，并提示用户
            time.sleep(0.2)  # 等待线程中先更新数据
            if self.write_frame_back_show_msg:
                show_msg = self.write_frame_back_show_msg
                self.ui.back_camera_video.setChecked(False)
                self.write_frame_back_show_msg = ''
                self.ui.back_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
            else:
                # 切换图片
                self.ui.back_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像开始.png)}")
                show_msg = '开始录像，路径:' + save_path
        # 结束录像
        else:
            self.ui.back_camera_video.setStyleSheet("QPushButton{border-image: url(:/icons/uuvImages/录像停止.png)}")
            self.is_write_frame_back = False
            self.write_frame_back_show_msg = ''
            show_msg = '结束录制'
            # 切换图片
        reply = QMessageBox.question(self, '提示', show_msg, QMessageBox.Close, QMessageBox.Close)

    # 初始化电机
    def init_motor(self):
        reply = QMessageBox.question(self, '提示', '初始化电机成功', QMessageBox.Close, QMessageBox.Close)
        #  控制往各个方向运动来初始化
        self.datamanager_obj.move = 0
        time.sleep(2)
        self.datamanager_obj.move = 1
        time.sleep(2)
        self.datamanager_obj.move = 2
        time.sleep(2)
        self.datamanager_obj.move = 5
        time.sleep(2)
        self.datamanager_obj.move = 6
        time.sleep(2)
        self.datamanager_obj.move = 0
        time.sleep(2)

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
    def save_video(self, front=True, save_path=None):
        """
        保存视频
        :param save_path:
        :param front:是否是前置摄像头
        :param start: 是否是开始保存 True开始 False 结束保存
        :return:
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if front:
            if isinstance(self.frame_front, np.ndarray):
                # print('self.frame_front', self.frame_front.shape)
                out = cv2.VideoWriter(save_path, fourcc, 10.0,
                                      (1920, 1080))  # 图像大小参数按（宽，高）一定得与写入帧大小一致
                while self.is_write_frame_front:
                    write_frame = copy.deepcopy(self.frame_front)
                    write_frame = cv2.resize(write_frame, (1920, 1080))
                    # 转为bgr  修改为已经是bgr不在转换
                    rgb_write_frame = write_frame[..., ::-1]
                    out.write(rgb_write_frame)
                    # print(time.time(), 'write frame', write_frame.shape)
                    time.sleep(0.1)
                out.release()
            else:
                self.write_frame_front_show_msg = '保存前摄没有数据'
                print('write_frame_front_show_msg', self.write_frame_front_show_msg)
                print('保存前摄没有数据')
        else:
            if isinstance(self.frame_back, np.ndarray):
                print('save', save_path)
                out = cv2.VideoWriter(save_path, fourcc, 10.0,
                                      (1920, 1080))  # 图像大小参数按（宽，高）一定得与写入帧大小一致
                while self.is_write_frame_back:
                    write_frame = copy.deepcopy(self.frame_back)
                    write_frame = cv2.resize(write_frame, (1920, 1080))
                    rgb_write_frame = write_frame[..., ::-1]
                    out.write(rgb_write_frame)
                    # print(time.time(), 'write frame', write_frame.shape)
                    time.sleep(0.1)
                out.release()
            else:
                print('保存后摄没有数据')
                self.write_frame_back_show_msg = '保存后摄没有数据'

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
        # 自稳
        elif keyevent.text() in ['r', 'R']:
            if self.datamanager_obj.is_auto:
                self.datamanager_obj.is_auto = 0
            else:
                self.datamanager_obj.is_auto = 1
        # 摄像头舵机
        elif keyevent.text() in ['y', 'Y']:
            self.datamanager_obj.camera = 2
        elif keyevent.text() in ['h', 'H']:
            self.datamanager_obj.camera = 0
        elif keyevent.text() in ['n', 'N']:
            self.datamanager_obj.camera = 8
        # 灯光
        elif keyevent.text() in ['t', 'T']:
            if self.datamanager_obj.light:
                self.datamanager_obj.light = 0
            else:
                self.datamanager_obj.light = 1
        # 声呐
        elif keyevent.text() in ['g', 'G']:
            if self.datamanager_obj.sonar:
                self.datamanager_obj.sonar = 0
            else:
                self.datamanager_obj.sonar = 1
        # 机械臂
        elif keyevent.text() in ['u', 'U']:
            self.datamanager_obj.arm = 1
        elif keyevent.text() in ['j', 'J']:
            self.datamanager_obj.arm = 0
        elif keyevent.text() in ['m', 'M']:
            self.datamanager_obj.arm = 4


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    main_windows = MainDialog()

    # main_windows.resize(1920, 1080)
    # main_windows.resize(1800, 700)
    main_windows.setStyleSheet("#MainWindow{border-image: url(:/icons/uuvImages/背景.png)}")  # 设置背景图 url(:/icons/uuvImages/录像停止.png)
    # main_windows.setStyleSheet("#MainWindow{border-image:url(uuvImages/背景.png);}")  # 设置背景图
    # setting_dlg = SettingWindow()
    # btn = main_windows.ui.setting_btn
    # btn.clicked.connect(setting_dlg.show)
    # apply_stylesheet(myapp, theme='dark_teal.xml')
    # apply_stylesheet(myapp, theme='light_red.xml')
    main_windows.show()
    sys.exit(myapp.exec_())



"""
生成res资源命令
pyrcc5 resource.qrc -o resource.py

"""