import socket
import logging
import time
logger = logging


class TcpClient:
    def __init__(self,ip=None,port=None):
        """
        tcp 客户端
        :param ip: 192.168.8.19
        :param port: 8080
        """
        if ip is None or port is None:
            import config
            self.target_host = config.tcp_server_ip  # 服务器端地址
            self.target_port = config.tcp_server_port  # 必须与服务器的端口号一致
        else:
            self.target_host = ip  # 服务器端地址
            self.target_port = port  # 必须与服务器的端口号一致
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.client.connect((self.target_host, self.target_port))
                break
            except Exception as e:
                print('error',e)
                continue

    def send(self, data):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.target_host, self.target_port))
        if not data:
            return
        self.client.send(data.encode())
        # response = self.client.recv(1024)
        # print(response)
        # self.client.close()

    def get(self):
        while True:
            response = self.client.recv(1024)
            str_response = str(response)[2:-1]
            if len(str_response) > 0:
                logger.info({'response': str_response})
            # 发送了开始
            print('response',response,'str_response',str_response)
            # self.send('error')
            time.sleep(2)


if __name__ == '__main__':
    tcp_client_obj = TcpClient(ip="192.168.8.19",port=5566)
    tcp_client_obj.get()
