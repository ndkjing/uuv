import socket
import json
import re
import time
import requests
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout
import threading

import config


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class TcpServer:
    def __init__(self):
        self.bind_ip = config.tcp_server_ip  # 监听所有可用的接口
        self.bind_port = config.tcp_server_port  # 非特权端口号都可以使用
        # AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 服务器监听的ip和端口号
        self.tcp_server_socket.bind((self.bind_ip, self.bind_port))
        print("[*] Listening on %s:%d" % (self.bind_ip, self.bind_port))
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 最大连接数
        self.tcp_server_socket.listen(128)
        # 是否有链接上
        self.b_connect = 0
        self.client = None
        # 罗盘角度
        self.theta_z = 0  # z轴角度
        self.theta_list = [0, 0, 0]  # 依次放 x,y,z 角度
        self.last_theta = 0
        # 深度
        self.deep = 0
        # 温度
        self.temperature = 0
        # 仓压
        self.press = 0
        # 是否漏水
        self.is_leak_water = 0
        # 大灯
        self.is_head_light = 0
        # led灯
        self.is_led_light = 0
        # 声呐
        self.is_sonar = 0
        # 摄像头角度
        self.camera_angle_pwm = 1500
        # 机械臂
        self.arm_pwm = 1500
        # 动力占比 %
        self.speed = 2

    def wait_connect(self):
        # 等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = self.tcp_server_socket.accept()
        print("客户端的ip地址和端口号为:", addr)
        self.b_connect = 1
        self.client = client

    def start_server(self):
        # 等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = self.tcp_server_socket.accept()
        print("客户端的ip地址和端口号为:", addr)
        print('time:', time.time())
        # 代码执行到此，说明客户端和服务端套接字建立连接成功
        print("[*] Acception connection from %s:%d" % (addr[0], addr[1]))
        while True:
            input_str = 'abcd'
            client.send(input_str.encode())
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
            time.sleep(0.5)

    # 客户处理线程
    def handle_client(self, client):
        recv_data = client.recv(1024)
        print("[*] Received: %s" % recv_data)
        # client_socket.send("hi~".encode())
        # recv_data = client_socket.recv(1024)
        # print("[*] Received: %s" % recv_data)
        # 向客户端返回数据
        data_len = len(recv_data)
        print("接收的数据长度为:", data_len)
        # 对二进制数据进行解码
        recv_content = recv_data.decode("gbk")
        print("接收客户端的数据:", recv_content)

    def close(self):
        self.tcp_server_socket.close()

    def write_data(self, data):
        self.client.send(data.encode())


class TcpServerQt(QWidget):
    def __init__(self):
        super(TcpServerQt, self).__init__()
        self.bind_ip = config.tcp_server_ip  # 监听所有可用的接口
        self.bind_port = config.tcp_server_port  # 非特权端口号都可以使用
        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.Any, config.tcp_server_port):
            self.browser.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)
        self.sock = None
        self.b_connect = 0
        # 罗盘角度
        self.theta_z = 0  # z轴角度
        self.theta_list = [0, 0, 0]  # 依次放 x,y,z 角度
        self.last_theta = 0
        # 深度
        self.deep = 0
        # 温度
        self.temperature = 0
        # 仓压
        self.press = 0
        # 是否漏水
        self.is_leak_water = 0
        # 大灯
        self.is_headlight = 0
        # led灯
        self.is_ledlight = 0
        # 声呐
        self.is_sonar = 0
        # 摄像头角度
        self.camera_angle_pwm = 1500
        # 机械臂
        self.arm_pwm = 1500
        # 动力占比 %
        self.speed = 2
        # 水下机器人运动方向
        self.move = 0
        self.pre_port = None

    def new_socket_slot(self):
        try:
            sock = self.server.nextPendingConnection()
            peer_address = sock.peerAddress().toString()
            peer_port = sock.peerPort()
            news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
            print('Connected with address {}, port {}'.format(peer_address, str(peer_port)))
            if self.pre_port is None:
                self.pre_port = peer_port
            elif peer_port - self.pre_port == 1:
                    # or peer_port - self.pre_port == 1:  self.pre_port is None:
                print('port2', peer_port)
                return
            sock.readyRead.connect(lambda: self.read_data_slot(sock))
            sock.disconnected.connect(lambda: self.disconnected_slot(sock))
            print('sock.isOpen()', sock.isOpen())
            self.sock = sock
            self.b_connect = 1
        except Exception as e:
            print('error', e)

    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            try:
                datagram = sock.read(sock.bytesAvailable())
                message = datagram.decode()
                # print('socket receive data', message)
                message = str(message)
                message = message.strip()
                press_find = re.findall(r'\"pressure\":(.*?),\"', message)
                if len(press_find) > 0:
                    self.press = float(press_find[0])

                water_find = re.findall(r'\"water\":(.*?),\"', message)
                if len(water_find) > 0:
                    self.is_leak_water = int(water_find[0])

                light_find = re.findall(r'\"light\":(.*?),\"', message)
                if len(light_find) > 0:
                    self.is_headlight = int(light_find[0])

                sonar_find = re.findall(r'\"sonar\":(.*?),\"', message)
                if len(sonar_find) > 0:
                    self.is_sonar = int(sonar_find[0])

                camera_find = re.findall(r'\"camera\":(.*?),\"', message)
                if len(camera_find) > 0:
                    self.camera_angle_pwm = int(camera_find[0])

                arm_find = re.findall(r'\"arm\":(.*?),\"', message)
                if len(arm_find) > 0:
                    self.arm_pwm = int(arm_find[0])

                pitch_find = re.findall(r'\"pitch\":(.*?),\"', message)
                if len(pitch_find) > 0:
                    self.theta_list[0] = float(pitch_find[0])

                roll_find = re.findall(r'\"roll\":(.*?),\"', message)
                if len(roll_find) > 0:
                    self.theta_list[1] = float(roll_find[0])

                yaw_find = re.findall(r'\"yaw\":(.*?),\"', message)
                if len(yaw_find) > 0:
                    self.theta_list[2] = float(yaw_find[0])
                    self.theta_z = self.theta_list[2]

                depth_find = re.findall(r'\"depth\":(.*?),\"', message)
                if len(depth_find) > 0:
                    self.deep = float(depth_find[0])

                tem_find = re.findall(r'\"tem\":(.*?),\"', message)
                if len(tem_find) > 0:
                    self.temperature = float(tem_find[0])

                speed_find = re.findall(r'\"speed\":(.*?),', message)
                if len(speed_find) > 0:
                    self.speed = int(speed_find[0])
                move_find = re.findall(r'\"move\":(.*?)}', message)
                if len(move_find) > 0:
                    self.move = int(move_find[0])
                # print('self.move',self.move)
                # print('self.press', self.deep, self.temperature, self.press, self.is_leak_water, self.is_headlight,
                #       self.is_sonar, self.camera_angle_pwm, self.arm_pwm, self.speed, self.move)
            except Exception as e:
                print('tcp data error', e)
                continue
            # answer = self.get_answer(message).replace('{br}', '\n')
            # new_datagram = answer.encode()

    def write_data(self, new_datagram):
        if self.sock:
            self.sock.write(new_datagram.encode())

    def get_answer(self, message):
        payload = {'key': 'free', 'appid': '0', 'msg': message}
        r = requests.get("http://api.qingyunke.com/api.php?", params=payload)
        answer = json.loads(r.text)['content']
        return answer

    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        print(news)
        sock.close()
        print('sock==self.sock', sock == self.sock)
        self.sock = None
        self.pre_port = None
        self.b_connect = 0

    def keyPressEvent(self, keyevent):
        if keyevent.text() in ['w', 'W']:
            print(keyevent.text())
            self.write_data('hello')


if __name__ == '__main__':
    obj = TcpServerQt()
    while True:
        time.sleep(1)
        print('1111')
    # obj.start_server()
