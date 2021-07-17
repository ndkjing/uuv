"""
水下机器人调试 streamlit
"""
import time
import streamlit as st
import threading
from dataManager import data_manager

time.sleep(0.1)
data_manager_obj = data_manager.DataManager()
forward = st.button('前进', key='1')
backward = st.button('后退', key='2')
left = st.button('左转')
right = st.button('右转')
rise = st.button('上升')
decline = st.button('下降')
shift_left = st.button('左移')
shift_right = st.button('右移')
stop = st.button('停止')
move = 0
if forward:
    move = 1
elif backward:
    move = 2
elif left:
    move = 3
elif right:
    move = 4
elif rise:
    move = 5
elif decline:
    move = 6
elif shift_left:
    move = 7
elif shift_right:
    move = 8
elif stop:
    move = 0
data_manager_obj.move = move
camera = st.slider('摄像头', min_value=0.0, max_value=1.0, step=0.1)  # 👈 this is a widget
data_manager_obj.camera = camera
arm = st.slider('机械臂', min_value=0.0, max_value=1.0, step=0.1)  # 👈 this is a widget
data_manager_obj.arm = arm
light = st.radio('灯光', ('打开', '关闭'), index=1)
data_manager_obj.light = 0 if light else 1
sonar = st.radio('声呐', ('打开', '关闭'), index=1)
data_manager_obj.sonar = 0 if sonar else 1

p = st.sidebar.slider('p', min_value=0.0, max_value=10.0, step=0.1)  # 👈 this is a widget
i = st.sidebar.slider('i', min_value=0.0, max_value=10.0, step=0.1)  # 👈 this is a widget
d = st.sidebar.slider('d', min_value=0.0, max_value=10.0, step=0.1)  # 👈 this is a widget
st.sidebar.write('p', p)
st.sidebar.write('i', i)
st.sidebar.write('d', d)
start_calibration = st.sidebar.button('开始校准')
end_calibration = st.sidebar.button('结束校准')
st.sidebar.write('客户端链接', data_manager_obj.tcp_server_obj.b_connect)
data_manager_obj.pid = [p, i, d]
if data_manager_obj.tcp_server_obj.b_connect and not data_manager_obj.is_start:
    get_tcp_data_thread = threading.Thread(target=data_manager_obj.get_tcp_data)
    send_tcp_data_thread = threading.Thread(target=data_manager_obj.send_tcp_data)
    joystick_thread = threading.Thread(target=data_manager_obj.joystick_obj.shoubin_thread)
    get_tcp_data_thread.start()
    send_tcp_data_thread.start()
    joystick_thread.start()
    data_manager_obj.is_start = 1

