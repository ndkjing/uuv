"""
水下机器人调试黑窗口
"""
import dataManager
import time
import threading


def main():
    data_manager_obj = dataManager.DataManager(only_joystick=True)
    get_tcp_data_thread = threading.Thread(target=data_manager_obj.get_tcp_data)
    send_tcp_data_thread = threading.Thread(target=data_manager_obj.send_tcp_data)
    joystick_thread = threading.Thread(target=data_manager_obj.joystick_obj.shoubin_thread)
    get_tcp_data_thread.start()
    send_tcp_data_thread.start()
    joystick_thread.start()


if __name__ == '__main__':
    main()
