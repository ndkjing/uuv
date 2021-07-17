import sys
import json
import time
import requests
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout
import threading


class TcpServer(QWidget):
    def __init__(self):
        super(TcpServer, self).__init__()
        self.resize(500, 450)
        # 1
        self.browser = QTextBrowser(self)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.browser)
        self.setLayout(self.v_layout)
        self.server = QTcpServer(self)
        if not self.server.listen(QHostAddress.AnyIPv4, 6666):
            self.browser.append(self.server.errorString())
        self.server.newConnection.connect(self.new_socket_slot)
        self.sock = None

    def new_socket_slot(self):
        sock = self.server.nextPendingConnection()
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Connected with address {}, port {}'.format(peer_address, str(peer_port))
        print('news', news)
        sock.readyRead.connect(lambda: self.read_data_slot(sock))
        sock.disconnected.connect(lambda: self.disconnected_slot(sock))
        self.sock = sock

    # 3
    def read_data_slot(self, sock):
        while sock.bytesAvailable():
            datagram = sock.read(sock.bytesAvailable())
            message = datagram.decode()
            print('receive data', message)
            # answer = self.get_answer(message).replace('{br}', '\n')
            # new_datagram = answer.encode()

    def write_data(self, new_datagram):
        time.sleep(0.1)
        print(self.sock)
        if self.sock:
            print(new_datagram)
            self.sock.write(new_datagram.encode())

    def get_answer(self, message):
        payload = {'key': 'free', 'appid': '0', 'msg': message}
        r = requests.get("http://api.qingyunke.com/api.php?", params=payload)
        answer = json.loads(r.text)['content']
        return answer

    # 4
    def disconnected_slot(self, sock):
        peer_address = sock.peerAddress().toString()
        peer_port = sock.peerPort()
        news = 'Disconnected with address {}, port {}'.format(peer_address, str(peer_port))
        self.browser.append(news)
        sock.close()

    def keyPressEvent(self, keyevent):
        print(f"键盘按键: {keyevent.text()},0X{keyevent.key():X} 被按下")
        if keyevent.text() == 'w' or keyevent.text() == 'W':
            print(keyevent.text())
            self.write_data('hello')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TcpServer()
    demo.show()
    sys.exit(app.exec_())
