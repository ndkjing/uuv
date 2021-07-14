import pygame
import threading
import time


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class Jostick:
    def __init__(self):
        self.clock = None
        self.count = None
        self.b_connect = 0
        self.axes_0 = None  #
        self.axes_1 = None  #
        self.axes_2 = None  #
        self.axes_3 = None  #
        self.b_light = 0  # 灯光开关
        self.b_sonar = 0  # 声呐开关
        self.arm = 0  # 机械臂打开量
        self.camera_steer = 0  # 摄像头舵机
        self.mode = 0  # 模式 0 手动 1 自稳
        self.init_joystick()
        self.reconnect = False

    def init_joystick(self):
        # 初始化
        pygame.init()
        pygame.joystick.init()
        self.clock = pygame.time.Clock()
        self.get_count()

    def get_count(self):
        self.count = pygame.joystick.get_count()

    def get_data(self):
        # 寻找电脑上的手柄数量，一般我只连了一个手柄（因为只有一个）
        for i in range(self.count):
            # 读取对应设备
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            while True:
                if self.count >= 1:
                    if not self.b_connect:
                        self.b_connect = 1
                        if self.reconnect:
                            self.init_joystick()
                            self.reconnect = False
                    # 这句话很重要，这是保障实时读取手柄摇杆信息，反正不能去掉
                    pygame.event.get()
                    # 获取摇杆数量
                    axes = joystick.get_numaxes()
                    for i in range(axes):
                        axis = round(joystick.get_axis(i), 2)
                        if i == 0:
                            self.axes_0 = axis
                            # print("0 ", axis)
                        if i == 1:
                            self.axes_1 = axis
                            # print("1 ", axis)
                        if i == 2:  # 上是负数
                            self.axes_2 = axis
                            # print("2 ", axis)
                        if i == 3:  # 左是负数
                            self.axes_3 = axis
                            # print("3 ", axis)
                    buttons = joystick.get_numbuttons()
                    button_input = [joystick.get_button(i) for i in range(buttons)]
                    if button_input[0] == 1:
                        self.b_light = 1 - self.b_light
                    if button_input[1] == 1:
                        self.b_sonar = 1 - self.b_sonar
                    if button_input[2] == 1:
                        self.mode = 1 - self.mode
                    if button_input[4] == 1:
                        if self.arm < 1:
                            self.arm += 0.05
                        else:
                            self.arm = 1
                        self.arm = round(self.arm, 2)
                    if button_input[6] == 1:
                        if self.arm > 0:
                            self.arm -= 0.05
                        else:
                            self.arm = 0
                        self.arm = round(self.arm, 2)
                    if button_input[5] == 1:
                        if self.camera_steer < 1:
                            self.camera_steer += 0.05
                        else:
                            self.camera_steer = 1
                        self.camera_steer = round(self.camera_steer, 2)
                    if button_input[7] == 1:
                        if self.camera_steer < 1:
                            self.camera_steer -= 0.05
                        else:
                            self.camera_steer = 0
                        self.camera_steer = round(self.camera_steer, 2)
                    # 获取键帽输入
                    # numhats = joystick.get_numhats()
                    # print('numhats', numhats,joystick.get_hat(0))
                    # for i  in range():
                    self.clock.tick(20)
                    time.sleep(0.001)
                    self.get_count()
                    # print('self.count', self.count)
                else:
                    if self.b_connect:
                        pygame.joystick.quit()
                        pygame.quit()
                        self.b_connect = 0
                        self.reconnect = True
                        time.sleep(2)
                        pygame.init()
                        pygame.joystick.init()
                    else:
                        # print(pygame.joystick.get_init())
                        # print(pygame.joystick.get_count())
                        # self.clock = pygame.time.Clock()
                        # time.sleep(1)
                        self.get_count()
                        # print('self.count', self.count)
                    time.sleep(0.1)


if __name__ == '__main__':
    obj = Jostick()
    t1 = threading.Thread(obj.get_data())
    t1.run()
    t1.join()
