import os
from common import utils

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
# tcp 服务器地址和端口
target_server_type = 4  # 0 1002 wifi地址  1 1002网线地址  2 家里wifi地址 其他 控制箱地址

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
# 1 qt tcp 2 tcp
tcp_server_type = 1


# 摄像头地址取决于设备 测试和实际地址不同
if target_server_type == 4:
    out_video=0  # 是否是内置
    if out_video:
        front_video_src = 'rtsp://192.168.2.5:8554/0'
        back_video_src = 'rtsp://192.168.2.6:8554/0'
    # 工业水下机器人内置摄像头
    else:
        front_video_src = 'rtsp://192.168.2.5:554/ch01.264'
        back_video_src = 'rtsp://192.168.2.6:8554/0'

# elif target_server_type == 1:
#     # front_video_src =0
#     front_video_src ="https://rtmp01open.ys7.com:9188/v3/openlive/F77671789_1_2.flv?expire=1670918205&id=392344446919000064&t=aa950e8c6b324d279086e1e552b5fc325bfd7749888a1b36e479206ef3011e0e&ev=100"
#     back_video_src ="rtmp://rtmp01open.ys7.com:1935/v3/openlive/F77671789_1_1?expire=1665729938&id=370583278005051392&t=1f89772b120962ae3f4f8e5ff794ece8127a9e53796c9599eb2b47584875bc70&ev=100"
else:
    # 公司 摄像头
    a = "rtmp://rtmp01open.ys7.com:1935/v3/openlive/F77671789_1_1?expire=1673004384&id=401094514567700480&t=3ae57ce5ae6a9ce391138b4567e3283d176573583862178671d8ada8ac1e7693&ev=100"
    # 厂房摄像头
    # b = "rtmp://rtmp01open.ys7.com:1935/v3/openlive/D50551834_1_2?expire=1665728758&id=370578328580620288&t=f2a7fc8cc13d3250b45bc5de20b7f49728cb84369039598d20a487318d441b72&ev=100"
    b = "dsad"
    front_video_src = a
    back_video_src = b

need_restart_joy = False
