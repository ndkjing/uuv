import json
import os
from common import utils
from storage import save_data

# 判读程序相对路径，在打包后变成用户文件夹里面层级太深
# root_path = os.path.dirname(os.path.abspath(__file__))
# 使用绝对路径 保存数据路径
disk_list = [r'D:\\', r'E:\\', r'F:\\']
root_path = None
for disk in disk_list:
    if os.path.exists(disk):
        root_path = os.path.join(disk, 'uuvSave')
        break
if root_path is None:
    root_path = os.path.join(r'C:\\', 'uuvSave')

save_dir = os.path.join(root_path, 'statics')
save_imgs_dir = os.path.join(save_dir, 'imgs')
save_videos_dir = os.path.join(save_dir, 'videos')
save_pid_path = os.path.join(save_dir, 'pid.json')  # 保存pid设置路径
save_angle_y_path = os.path.join(save_imgs_dir, 'angle_y.png')  # 保存pid设置路径
save_angle_z_path = os.path.join(save_imgs_dir, 'angle_z.png')  # 保存pid设置路径
if not os.path.exists(root_path):
    os.mkdir(root_path)
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
if not os.path.exists(save_imgs_dir):
    os.mkdir(save_imgs_dir)
if not os.path.exists(save_videos_dir):
    os.mkdir(save_videos_dir)
# 保存摄像头地址路径
disk_list_video = [r'C:\\', r'D:\\', r'E:\\', r'F:\\']
root_path_video = None
for disk_video in disk_list_video:
    if os.path.exists(disk_video):
        root_path_video = os.path.join(disk_video, 'uuvSave')
        break
if not os.path.exists(root_path_video):
    os.mkdir(root_path_video)
save_video_path = os.path.join(root_path_video, 'video.json')
save_img_path = os.path.join(root_path_video, 'img.json')

# tcp 服务器地址和端口
target_server_type = 1  # 0 1002 wifi地址  1 1002网线地址  2 家里wifi地址 其他 控制箱地址
if target_server_type == 0:
    server_ip = '192.168.199.222'
elif target_server_type == 1:
    server_ip = '192.168.8.19'
    # server_ip = '127.0.0.1'
elif target_server_type == 2:
    server_ip = '192.168.1.8'
else:
    server_ip = '192.168.2.2'
server_port = 5566
# tcp_server_ip = utils.get_host_ip() # 自动获取ip
tcp_server_ip = server_ip
tcp_server_port = 5566
only_joystick = 1  # 是否只是用手柄不适用键盘  0 都是用  1 只是用手柄
# 1 qt tcp   ；2 tcp
tcp_server_type = 1
out_video = 0  # 设置是内置还是外置摄像头  0:外置   1:外置    2:内置小摄像头
back_video = 0  # 设置是否有后置摄像头(后摄有的话肯定是外置)     0: 没有   1: 有
# 摄像头地址取决于设备测试和实际地址不同
if target_server_type == 4:
    if out_video == 0:
        front_video_src = 'rtsp://192.168.2.5:8554/0'
        if back_video:
            back_video_src = 'rtsp://192.168.2.6:8554/0'
        else:
            back_video_src = ''
    # 工业水下机器人内置摄像头
    else:
        front_video_src = 'rtsp://192.168.2.5:554/ch01.264'
        if back_video:
            back_video_src = 'rtsp://192.168.2.6:8554/0'
        else:
            back_video_src = ''
else:
    # 公司 摄像头
    front_video_src = "rtsp://192.168.2.5:554/h264/ch1/main/av_stream"
    back_video_src = ""
# 根据软件设置页面修改动态修改摄像头地址
video_src_dict = {
    'f': {
        0: 'rtsp://192.168.2.5:8554/0',
        1: 'rtsp://192.168.2.5:554/ch01.264',
        2: 'rtsp://192.168.2.5:554/h264/ch1/main/av_stream'
    },
    'b': {
        0: '',
        1: 'rtsp://192.168.2.6:8554/0'
    }
}
need_restart_joy = False  # 是否需要重新检测手柄是否存在
control_method = 2  # 控制方式1单个通道控制  控制方式2两个通道控制
video_json = save_data.get_data(save_video_path)
if video_json:
    print('video json', video_json)
    out_video = int(video_json['f'])
    back_video = int(video_json['b'])
    control_method = int(video_json['c'])
    front_video_src = video_src_dict['f'][video_json['f']]
    back_video_src = video_src_dict['b'][video_json['b']]
    # front_video_src = "rtsp://192.168.1.168:554/h264/ch1/main/av_stream"  # 测试用摄像头地址

# camera_ip = '192.168.1.168'  # 测试用
camera_ip = '192.168.2.5'
img_path = ''
img_json = save_data.get_data(save_img_path)
if img_json:
    img_path = img_json['img_path']
