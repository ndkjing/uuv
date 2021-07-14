"""
数据管理
"""
import time
import tcpServer
import dataDefine
import joystick
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
    def __init__(self, only_joystick=False):
        self.tcp_server_obj = tcpServer.TcpServer()
        self.joystick_obj = joystick.Jostick()
        self.move = 0
        self.speed = 0.5  # 速度
        self.camera = 0
        self.light = 0
        self.sonar = 0
        self.arm = 0
        self.pid = [0, 0, 0]
        self.pid_v = [0, 0, 0]
        self.backup_pwm = [0, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.receive_pwm = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.compass = [0, 0, 0]
        self.deep = None  # 深度
        self.pressure = None  # 仓压
        self.temperature = None  # 水温度
        self.b_leak = None  # 是否漏水
        self.is_start = 0  # 是否已开启
        self.only_joystick = only_joystick
        # self.init_run()

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
            if self.joystick_obj.axes_0 and abs(self.joystick_obj.axes_0) > 0.2:
                if self.joystick_obj.axes_0 > 0:
                    joy_move = 8
                else:
                    joy_move = 7
                joy_speed = abs(self.joystick_obj.axes_0)
            elif self.joystick_obj.axes_1 and abs(self.joystick_obj.axes_1) > 0.2:
                if self.joystick_obj.axes_1 > 0:
                    joy_move = 2
                else:
                    joy_move = 1
                joy_speed = abs(self.joystick_obj.axes_0)
            elif self.joystick_obj.axes_2 and abs(self.joystick_obj.axes_2) > 0.2:
                if self.joystick_obj.axes_2 > 0:
                    joy_move = 4
                else:
                    joy_move = 3
                joy_speed = abs(self.joystick_obj.axes_0)
            elif self.joystick_obj.axes_3 and abs(self.joystick_obj.axes_3) > 0.2:
                if self.joystick_obj.axes_3 > 0:
                    joy_move = 6
                else:
                    joy_move = 5
                joy_speed = abs(self.joystick_obj.axes_0)
            else:
                joy_move = 0
                joy_speed = 0
            if joy_move != 0:
                move_info = 'move%sz' % joy_move
                speed_info = 'speed%sz' % joy_speed
            elif self.only_joystick:
                move_info = 'move%sz' % joy_move
                speed_info = 'speed%sz' % joy_speed
            else:
                move_info = 'move%sz' % self.move
                speed_info = 'speed%sz' % self.speed
            camera_info = 'camera%sz' % self.joystick_obj.camera_steer
            light_info = 'light%sz' % self.joystick_obj.b_light
            sonar_info = 'sonar%sz' % self.joystick_obj.b_sonar
            arm_info = 'arm%sz' % self.joystick_obj.arm
            pid_info = 'pid%s,%s,%sz' % (self.pid[0], self.pid[1], self.pid[2])
            backup_pwm_info = 'backupPwm%sz' % self.backup_pwm
            try:
                self.tcp_server_obj.client.send(move_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(speed_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(camera_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(light_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(sonar_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(arm_info.encode())
                time.sleep(0.01)
                self.tcp_server_obj.client.send(pid_info.encode())
            except ConnectionResetError as e:
                self.tcp_server_obj.client.close()
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
            # TODO 解析tcp数据复制给 compass等

if __name__ == '__main__':
    data_manager_obj = DataManager()
    time.sleep(0.1)
    data_manager_obj1 = DataManager()
