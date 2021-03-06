"""
数据管理
"""
import time
from common import tcpServer
# from driver import joystick_no_pygame as joystick
from driver import joystick
import config
import threading


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class DataManager(object):
    def __init__(self):
        self.tcp_server_obj = tcpServer.TcpServerQt()
        # if config.tcp_server_type == 1:
        #     self.tcp_server_obj = tcpServer.TcpServerQt()
        # else:
        #     self.tcp_server_obj = tcpServer.TcpServer()
        self.joystick_obj = joystick.JoyManager()
        # 自稳 0 非自稳 1 自稳  稳定深度和x,y,z角度
        self.is_auto = 0
        # 滑动条油门
        self.speed_slider_value = 1
        self.deep_slider_value = 0
        self.angle_slider_value = 0
        self.move = 0
        self.speed = 2  # 油门大小 1-4
        self.camera = 0
        self.light = 0
        self.sonar = 0
        self.arm = 0
        self.pid = [0, 0, 0]
        self.pid_v = [0, 0, 0]
        self.backup_pwm = [0, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.receive_pwm = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.is_start = 0  # 是否已开启
        self.b_keep_deep = 0
        self.b_move_deep = 0
        self.b_keep_direction = 0
        self.b_move_direction = 0

    def init_run(self):
        t1 = threading.Thread(target=self.tcp_server_obj.wait_connect)
        t1.setDaemon(True)
        t1.run()

    # 发送tcp数据
    def send_tcp_data(self, b_once=False):
        while True:
            time.sleep(0.05)
            if not self.tcp_server_obj.b_connect:
                continue
            # if self.joystick_obj.axes_0 and abs(self.joystick_obj.axes_0) > 0.2:
            #     if self.joystick_obj.axes_0 > 0:
            #         joy_move = 8
            #     else:
            #         joy_move = 7
            #     joy_speed = abs(self.joystick_obj.axes_0)
            # elif self.joystick_obj.axes_1 and abs(self.joystick_obj.axes_1) > 0.2:
            #     if self.joystick_obj.axes_1 > 0:
            #         joy_move = 2
            #     else:
            #         joy_move = 1
            #     joy_speed = abs(self.joystick_obj.axes_0)
            # elif self.joystick_obj.axes_2 and abs(self.joystick_obj.axes_2) > 0.2:
            #     if self.joystick_obj.axes_2 > 0:
            #         joy_move = 4
            #     else:
            #         joy_move = 3
            #     joy_speed = abs(self.joystick_obj.axes_0)
            # elif self.joystick_obj.axes_3 and abs(self.joystick_obj.axes_3) > 0.2:
            #     if self.joystick_obj.axes_3 > 0:
            #         joy_move = 6
            #     else:
            #         joy_move = 5
            #     joy_speed = abs(self.joystick_obj.axes_0)
            # else:
            #     joy_move = 0
            #     joy_speed = 0
            # print('joy_move', joy_move)
            # if joy_move != 0:
            #     move_info = 'move%sz' % joy_move
            #     speed_info = 'speed%sz' % joy_speed
            # elif config.only_joystick:
            #     move_info = 'move%sz' % joy_move
            #     speed_info = 'speed%sz' % joy_speed
            if config.only_joystick:
                move_info = 'move%sz' % self.joystick_obj.joy_obj.move
                speed_info = 'speed%sz' % self.joystick_obj.joy_obj.speed
                camera_info = 'camera%sz' % self.joystick_obj.joy_obj.camera_steer
                light_info = 'light%sz' % self.joystick_obj.joy_obj.b_ledlight
                sonar_info = 'sonar%sz' % self.joystick_obj.joy_obj.b_sonar
                arm_info = 'arm%sz' % self.joystick_obj.joy_obj.arm
                pid_info = 'pid%s,%s,%sz' % (self.pid[0], self.pid[1], self.pid[2])
                mode_info = 'mode%sz' % self.joystick_obj.joy_obj.mode
                head_info = 'head%sz' % self.joystick_obj.joy_obj.b_headlight
                backup_pwm_info = 'backupPwm%sz' % self.backup_pwm
            else:
                move_info = 'move%sz' % self.move
                speed_info = 'speed%sz' % self.speed_slider_value
                camera_info = 'camera%sz' % self.camera
                light_info = 'light%sz' % self.light
                sonar_info = 'sonar%sz' % self.sonar
                arm_info = 'arm%sz' % self.arm
                pid_info = 'pid%s,%s,%sz' % (self.pid[0], self.pid[1], self.pid[2])
                mode_info = 'mode%sz' % (self.is_auto)
                head_info = 'head%sz' % (self.joystick_obj.joy_obj.b_headlight)
                backup_pwm_info = 'backupPwm%sz' % self.backup_pwm
            send_data_list = []
            # camera_info = 'camera%sz' % self.joystick_obj.camera_steer
            # light_info = 'light%sz' % self.joystick_obj.b_light
            # sonar_info = 'sonar%sz' % self.joystick_obj.b_sonar
            # arm_info = 'arm%sz' % self.joystick_obj.arm

            send_data_method = 1
            send_data_list.append(sonar_info)
            send_data_list.append(arm_info)
            send_data_list.append(light_info)
            send_data_list.append(camera_info)
            send_data_list.append(speed_info)
            send_data_list.append(move_info)
            # send_data_list.append(pid_info)
            send_data_list.append(mode_info)
            send_data_list.append(head_info)
            try:
                if send_data_method == 1:
                    for data in send_data_list:
                        # if 'move' not in data:
                        #     continue
                        # print('send data', data)
                        self.tcp_server_obj.write_data(data)
                        time.sleep(0.005)
                else:
                    pass
            except ConnectionResetError as e:
                print('tcp_server_obj.write_data', e)
                self.tcp_server_obj.client.disconnected_slot()
            if b_once:
                return

    # 接受tcp数据
    def get_tcp_data(self):
        while True:
            time.sleep(0.1)
            if not self.tcp_server_obj.b_connect:
                continue
            recv_data = self.tcp_server_obj.client.recv(1024)
            print("[*] Received: %s" % recv_data)


if __name__ == '__main__':
    data_manager_obj = DataManager()
    time.sleep(0.1)
    data_manager_obj1 = DataManager()
