# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.arm_label = QtWidgets.QLabel(self.groupBox_7)
        self.arm_label.setObjectName("arm_label")
        self.horizontalLayout_5.addWidget(self.arm_label)
        self.camera_steer_label = QtWidgets.QLabel(self.groupBox_7)
        self.camera_steer_label.setObjectName("camera_steer_label")
        self.horizontalLayout_5.addWidget(self.camera_steer_label)
        self.sonar_label = QtWidgets.QLabel(self.groupBox_7)
        self.sonar_label.setObjectName("sonar_label")
        self.horizontalLayout_5.addWidget(self.sonar_label)
        self.light_label = QtWidgets.QLabel(self.groupBox_7)
        self.light_label.setObjectName("light_label")
        self.horizontalLayout_5.addWidget(self.light_label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.logo_label = QtWidgets.QLabel(self.groupBox_7)
        self.logo_label.setObjectName("logo_label")
        self.horizontalLayout_5.addWidget(self.logo_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.leak_label = QtWidgets.QLabel(self.groupBox_7)
        self.leak_label.setObjectName("leak_label")
        self.horizontalLayout_5.addWidget(self.leak_label)
        self.motor_lock_label = QtWidgets.QLabel(self.groupBox_7)
        self.motor_lock_label.setObjectName("motor_lock_label")
        self.horizontalLayout_5.addWidget(self.motor_lock_label)
        self.speed_label = QtWidgets.QLabel(self.groupBox_7)
        self.speed_label.setObjectName("speed_label")
        self.horizontalLayout_5.addWidget(self.speed_label)
        self.pressure_label = QtWidgets.QLabel(self.groupBox_7)
        self.pressure_label.setObjectName("pressure_label")
        self.horizontalLayout_5.addWidget(self.pressure_label)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.setting_btn = QtWidgets.QPushButton(self.groupBox)
        self.setting_btn.setObjectName("setting_btn")
        self.horizontalLayout_2.addWidget(self.setting_btn)
        self.init_motor_btn = QtWidgets.QPushButton(self.groupBox)
        self.init_motor_btn.setObjectName("init_motor_btn")
        self.horizontalLayout_2.addWidget(self.init_motor_btn)
        self.open_sonar_btn = QtWidgets.QPushButton(self.groupBox)
        self.open_sonar_btn.setObjectName("open_sonar_btn")
        self.horizontalLayout_2.addWidget(self.open_sonar_btn)
        self.switch_video_button = QtWidgets.QPushButton(self.groupBox)
        self.switch_video_button.setObjectName("switch_video_button")
        self.horizontalLayout_2.addWidget(self.switch_video_button)
        self.show_video_button = QtWidgets.QPushButton(self.groupBox)
        self.show_video_button.setObjectName("show_video_button")
        self.horizontalLayout_2.addWidget(self.show_video_button)
        self.temperature_label = QtWidgets.QLabel(self.groupBox)
        self.temperature_label.setObjectName("temperature_label")
        self.horizontalLayout_2.addWidget(self.temperature_label)
        self.deep_label = QtWidgets.QLabel(self.groupBox)
        self.deep_label.setObjectName("deep_label")
        self.horizontalLayout_2.addWidget(self.deep_label)
        self.joystick_label = QtWidgets.QLabel(self.groupBox)
        self.joystick_label.setObjectName("joystick_label")
        self.horizontalLayout_2.addWidget(self.joystick_label)
        self.mode_label = QtWidgets.QLabel(self.groupBox)
        self.mode_label.setLineWidth(3)
        self.mode_label.setObjectName("mode_label")
        self.horizontalLayout_2.addWidget(self.mode_label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.back_camera_video = QtWidgets.QPushButton(self.groupBox)
        self.back_camera_video.setObjectName("back_camera_video")
        self.horizontalLayout_2.addWidget(self.back_camera_video)
        self.back_camera_cap = QtWidgets.QPushButton(self.groupBox)
        self.back_camera_cap.setObjectName("back_camera_cap")
        self.horizontalLayout_2.addWidget(self.back_camera_cap)
        self.back_label = QtWidgets.QLabel(self.groupBox)
        self.back_label.setObjectName("back_label")
        self.horizontalLayout_2.addWidget(self.back_label)
        self.front_camera_video = QtWidgets.QPushButton(self.groupBox)
        self.front_camera_video.setObjectName("front_camera_video")
        self.horizontalLayout_2.addWidget(self.front_camera_video)
        self.front_camera_cap = QtWidgets.QPushButton(self.groupBox)
        self.front_camera_cap.setObjectName("front_camera_cap")
        self.horizontalLayout_2.addWidget(self.front_camera_cap)
        self.front_label = QtWidgets.QLabel(self.groupBox)
        self.front_label.setObjectName("front_label")
        self.horizontalLayout_2.addWidget(self.front_label)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.back_video_label = QtWidgets.QLabel(self.groupBox_5)
        self.back_video_label.setObjectName("back_video_label")
        self.horizontalLayout_4.addWidget(self.back_video_label)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.x_y_z_box = QtWidgets.QGroupBox(self.groupBox_6)
        self.x_y_z_box.setTitle("")
        self.x_y_z_box.setObjectName("x_y_z_box")
        self.x_y_z_layout = QtWidgets.QHBoxLayout(self.x_y_z_box)
        self.x_y_z_layout.setContentsMargins(0, 0, 0, 0)
        self.x_y_z_layout.setSpacing(0)
        self.x_y_z_layout.setObjectName("x_y_z_layout")
        self.angle_y_label = QtWidgets.QLabel(self.x_y_z_box)
        self.angle_y_label.setObjectName("angle_y_label")
        self.x_y_z_layout.addWidget(self.angle_y_label)
        self.angle_z_label = QtWidgets.QLabel(self.x_y_z_box)
        self.angle_z_label.setObjectName("angle_z_label")
        self.x_y_z_layout.addWidget(self.angle_z_label)
        self.x_y_z_layout.setStretch(0, 1)
        self.x_y_z_layout.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.x_y_z_box)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_15 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_15.setTitle("")
        self.groupBox_15.setObjectName("groupBox_15")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_15)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.slider_label = QtWidgets.QLabel(self.groupBox_15)
        self.slider_label.setAlignment(QtCore.Qt.AlignCenter)
        self.slider_label.setObjectName("slider_label")
        self.verticalLayout_5.addWidget(self.slider_label)
        self.verticalLayout_4.addWidget(self.groupBox_15)
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_12.setTitle("")
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.speed_radio_button = QtWidgets.QRadioButton(self.groupBox_12)
        self.speed_radio_button.setChecked(True)
        self.speed_radio_button.setObjectName("speed_radio_button")
        self.horizontalLayout_7.addWidget(self.speed_radio_button)
        self.speed_slider = QtWidgets.QSlider(self.groupBox_12)
        self.speed_slider.setToolTipDuration(1)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(4)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setProperty("value", 4)
        self.speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.speed_slider.setObjectName("speed_slider")
        self.horizontalLayout_7.addWidget(self.speed_slider)
        self.speed_slider_label = QtWidgets.QLabel(self.groupBox_12)
        self.speed_slider_label.setObjectName("speed_slider_label")
        self.horizontalLayout_7.addWidget(self.speed_slider_label)
        self.verticalLayout_4.addWidget(self.groupBox_12)
        self.groupBox_13 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_13.setTitle("")
        self.groupBox_13.setObjectName("groupBox_13")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.deep_radio_button = QtWidgets.QRadioButton(self.groupBox_13)
        self.deep_radio_button.setObjectName("deep_radio_button")
        self.horizontalLayout_8.addWidget(self.deep_radio_button)
        self.deep_slider = QtWidgets.QSlider(self.groupBox_13)
        self.deep_slider.setOrientation(QtCore.Qt.Horizontal)
        self.deep_slider.setObjectName("deep_slider")
        self.horizontalLayout_8.addWidget(self.deep_slider)
        self.deep_slider_label = QtWidgets.QLabel(self.groupBox_13)
        self.deep_slider_label.setObjectName("deep_slider_label")
        self.horizontalLayout_8.addWidget(self.deep_slider_label)
        self.verticalLayout_4.addWidget(self.groupBox_13)
        self.groupBox_14 = QtWidgets.QGroupBox(self.groupBox_9)
        self.groupBox_14.setTitle("")
        self.groupBox_14.setObjectName("groupBox_14")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_14)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.angle_radio_button = QtWidgets.QRadioButton(self.groupBox_14)
        self.angle_radio_button.setObjectName("angle_radio_button")
        self.horizontalLayout_9.addWidget(self.angle_radio_button)
        self.angle_slider = QtWidgets.QSlider(self.groupBox_14)
        self.angle_slider.setMaximum(360)
        self.angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.angle_slider.setObjectName("angle_slider")
        self.horizontalLayout_9.addWidget(self.angle_slider)
        self.angle_slider_label = QtWidgets.QLabel(self.groupBox_14)
        self.angle_slider_label.setObjectName("angle_slider_label")
        self.horizontalLayout_9.addWidget(self.angle_slider_label)
        self.verticalLayout_4.addWidget(self.groupBox_14)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 2)
        self.verticalLayout_4.setStretch(2, 2)
        self.verticalLayout_4.setStretch(3, 2)
        self.verticalLayout_3.addWidget(self.groupBox_9)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.front_video_label = QtWidgets.QLabel(self.groupBox_2)
        self.front_video_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.front_video_label.setObjectName("front_video_label")
        self.horizontalLayout_3.addWidget(self.front_video_label)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionbse = QtWidgets.QAction(MainWindow)
        self.actionbse.setObjectName("actionbse")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "水下机器人"))
        self.arm_label.setText(_translate("MainWindow", "机械臂"))
        self.camera_steer_label.setText(_translate("MainWindow", "舵机"))
        self.sonar_label.setText(_translate("MainWindow", "声呐"))
        self.light_label.setText(_translate("MainWindow", "灯："))
        self.logo_label.setText(_translate("MainWindow", "行星轮"))
        self.leak_label.setText(_translate("MainWindow", "漏水"))
        self.motor_lock_label.setText(_translate("MainWindow", "解锁："))
        self.speed_label.setText(_translate("MainWindow", "动力："))
        self.pressure_label.setText(_translate("MainWindow", "仓压："))
        self.setting_btn.setText(_translate("MainWindow", "设置"))
        self.init_motor_btn.setText(_translate("MainWindow", "解锁"))
        self.open_sonar_btn.setText(_translate("MainWindow", "声呐"))
        self.switch_video_button.setText(_translate("MainWindow", "切换"))
        self.show_video_button.setText(_translate("MainWindow", "显示视频"))
        self.temperature_label.setText(_translate("MainWindow", "水温"))
        self.deep_label.setText(_translate("MainWindow", "深度"))
        self.joystick_label.setText(_translate("MainWindow", "遥控"))
        self.mode_label.setText(_translate("MainWindow", "模式："))
        self.back_camera_video.setText(_translate("MainWindow", "录像"))
        self.back_camera_cap.setText(_translate("MainWindow", "截图"))
        self.back_label.setText(_translate("MainWindow", "后摄"))
        self.front_camera_video.setText(_translate("MainWindow", "录像"))
        self.front_camera_cap.setText(_translate("MainWindow", "截图"))
        self.front_label.setText(_translate("MainWindow", "前摄"))
        self.back_video_label.setText(_translate("MainWindow", "后摄"))
        self.angle_y_label.setText(_translate("MainWindow", "横滚"))
        self.angle_z_label.setText(_translate("MainWindow", "偏航"))
        self.slider_label.setText(_translate("MainWindow", "滑动调节条"))
        self.speed_radio_button.setText(_translate("MainWindow", "使能"))
        self.speed_slider_label.setText(_translate("MainWindow", "油门："))
        self.deep_radio_button.setText(_translate("MainWindow", "使能"))
        self.deep_slider_label.setText(_translate("MainWindow", "深度："))
        self.angle_radio_button.setText(_translate("MainWindow", "使能"))
        self.angle_slider_label.setText(_translate("MainWindow", "角度："))
        self.front_video_label.setText(_translate("MainWindow", "前摄"))
        self.actionbse.setText(_translate("MainWindow", "base"))
import res_rc
