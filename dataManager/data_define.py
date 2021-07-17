"""
无人船数据定义
"""


class DataDefine:
    def __init__(self):
        self.move = 0
        self.camera = 0
        self.light = 0
        self.sonar = 0
        self.arm = 0
        self.pid = [0, 0, 0]
        self.backup_pwm = [0, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.receive_pwm = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.compass = [0, 0, 0]
