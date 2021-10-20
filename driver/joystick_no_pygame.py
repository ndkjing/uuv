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
        self.count = 0
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
        # self.init_joystick()
        self.reconnect = False


    def get_data(self, is_debug=False):
        """
        获取数据
        :param is_debug:False不打印数据 True print获取到的数据
        :return:
        """
        while True:
            time.sleep(1)


if __name__ == '__main__':
    obj = Jostick()
    obj.get_data(is_debug=True)
    # t1 = threading.Thread(obj.get_data())
    # t1.run()
    # while True:
    #     time.sleep(1)
