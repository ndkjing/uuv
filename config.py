import os
from common import utils

# 判读程序相对路径，在打包后变成用户文件夹里面层级太深
# root_path = os.path.dirname(os.path.abspath(__file__))
# 使用绝对路径
disk_list = [r'D:\\',r'E:\\',r'F:\\']
root_path = None
for disk in disk_list:
    if os.path.exists(disk):
        root_path = os.path.join(disk,'uuvSave')
        break
if root_path is None:
    root_path = os.path.join(r'C:\\','uuvSave')

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
    server_ip = '192.168.9.19'
elif target_server_type == 2:
    server_ip = '192.168.1.8'
else:
    server_ip = '192.168.2.2'
server_port = 5566
# tcp_server_ip = utils.get_host_ip() # 自动获取ip
tcp_server_ip = server_ip
tcp_server_port = 5566
only_joystick=0  # 是否只是用手柄不适用键盘  0 都是用  1 只是用手柄
#1 qt tcp 2 tcp
tcp_server_type = 1
front_video_src = 'rtmp://rtmp01open.ys7.com:1935/v3/openlive/F77671789_1_1?expire=1665304393&id=368798413455241216&t=7a806071f327825e868312b6a548bb01cf94dbf124112d419f0d97d5cebb658b&ev=100'
back_video_src = 'rtmp://rtmp01open.ys7.com:1935/v3/openlive/F77671789_1_2?expire=1665304424&id=368798544144896000&t=da324d4dae71831cccea1da78705bd48ca3037546d4d360754fc5664a0358aa6&ev=100'
# front_video_src = r'F:\软件相关\开发软件\ffmpeg\bin\ffmpeg_test.flv'
# back_video_src = r'F:\软件相关\开发软件\ffmpeg\bin\ffmpeg_test.flv'