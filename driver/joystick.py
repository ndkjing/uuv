import pygame
import threading
import time
from collections import deque


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


threshold = 0.7


@Singleton
class Jostick:
    def __init__(self):
        self.clock = None
        self.count = 0
        self.b_connect = 0
        self.axes_0 = None  #
        self.axes_1 = None  #
        self.axes_2 = None  #
        self.axes_3 = None  #
        self.move = 0  # 运动方向
        self.b_ledlight = 0  # led灯开关(pwm灯)
        self.b_sonar = 0  # 声呐开关
        self.b_headlight = 0  # 大灯开关
        self.mode = 0  # 模式 0 手动 1 自稳
        self.max_len = 2
        self.b_ledlight_list = deque(maxlen=self.max_len)
        self.b_sonar_list = deque(maxlen=self.max_len)
        self.b_headlight_list = deque(maxlen=self.max_len)
        self.mode_list = deque(maxlen=self.max_len)
        self.arm = 0  # 机械臂打开量
        self.camera_steer = 0  # 摄像头舵机
        self.speed = 2  # 动力0 1 2 3 4  对应动力0%  25%  50%  75%  100%
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
        # print('self.count', self.count)

    def get_data(self, is_debug=False):
        """
        获取数据
        :param is_debug:False不打印数据 True print获取到的数据
        :return:
        """
        # 寻找电脑上的手柄数量
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
                        if i == 1:
                            self.axes_1 = axis
                        if i == 2:  # 上是负数
                            self.axes_2 = axis
                        if i == 3:  # 左是负数
                            self.axes_3 = axis
                        # 根据按钮值判断运动方向
                        """
                        0：停止
                        1：前进
                        2：后退
                        3：左转
                        4：右转
                        5：上升
                        6：下降
                        7:左移
                        8:右移
                        """
                    # print('self.axes_0,self.axes_1,self.axes_2,self.axes_3',self.axes_0,self.axes_1,self.axes_2,self.axes_3)
                    if abs(self.axes_0) < threshold and abs(self.axes_1) < threshold and abs(
                            self.axes_2) < threshold and abs(
                        self.axes_3) < threshold:
                        self.move = 0
                    elif abs(self.axes_0) < threshold and abs(self.axes_1) < threshold:
                        if self.axes_2 >= threshold:
                            self.move = 8
                        elif self.axes_2 <= -threshold:
                            self.move = 7
                        if self.axes_3 >= threshold:
                            self.move = 6
                        elif self.axes_3 <= -threshold:
                            self.move = 5
                    elif abs(self.axes_2) < threshold and abs(self.axes_3) < threshold:
                        if self.axes_0 >= threshold:
                            self.move = 4
                        elif self.axes_0 <= -threshold:
                            self.move = 3
                        if self.axes_1 >= threshold:
                            self.move = 2
                        elif self.axes_1 <= -threshold:
                            self.move = 1
                    # print('self.move', self.move)
                    buttons = joystick.get_numbuttons()
                    button_input = [joystick.get_button(i) for i in range(buttons)]
                    # print('button_input', button_input)
                    # pwm led灯
                    if button_input[0] == 1 and button_input[8] == 1:
                        self.b_ledlight = 1
                    elif button_input[0] == 1:
                        self.b_ledlight = 0
                    # 声呐
                    if button_input[1] == 1 and button_input[8] == 1:
                        self.b_sonar = 1
                    elif button_input[1] == 1:
                        self.b_sonar = 0
                    # 大灯
                    if button_input[2] == 1 and button_input[8] == 1:
                        self.b_headlight = 1
                    elif button_input[2] == 1:
                        self.b_headlight = 0
                    # 自稳
                    if button_input[3] == 1 and button_input[8] == 1:
                        self.mode = 1
                    elif button_input[3] == 1:
                        self.mode = 0
                    if button_input[4] == 1:
                        self.arm = 1
                    if button_input[6] == 1:
                        self.arm = 4
                    if button_input[4] == 0 and button_input[6] == 0:
                        self.arm = 0
                    if button_input[5] == 1:
                        self.camera_steer = 2
                    if button_input[7] == 1:
                        self.camera_steer = 8
                    if button_input[5] == 0 and button_input[7] == 0:
                        self.camera_steer = 0
                    # print(time.time(),
                    #       'self.b_ledlight,self.b_sonar,self.b_headlight,self.mode,self.arm,self.camera_steer',
                    #       self.b_ledlight, self.b_sonar, self.b_headlight, self.mode, self.arm, self.camera_steer)
                    # 获取键帽输入
                    numhats = joystick.get_numhats()
                    for i in range(numhats):
                        if joystick.get_hat(i)[1] == 1:
                            self.speed = 1
                        elif joystick.get_hat(i)[1] == -1:
                            self.speed = 3
                        elif joystick.get_hat(i)[0] == 1:
                            self.speed = 2
                        elif joystick.get_hat(i)[0] == -1:
                            self.speed = 4
                    # print('self.speed', self.speed)
                    self.clock.tick(20)
                    # time.sleep(0.001)
                    self.get_count()
                    # print('self.count', self.count)
                else:
                    print('self.count', self.count)
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
    obj.get_data(is_debug=True)
    # t1 = threading.Thread(obj.get_data())
    # t1.run()
    # while True:
    #     time.sleep(1)
