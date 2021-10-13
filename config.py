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
if not os.path.exists(root_path):
    os.mkdir(root_path)
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
if not os.path.exists(save_imgs_dir):
    os.mkdir(save_imgs_dir)
if not os.path.exists(save_videos_dir):
    os.mkdir(save_videos_dir)
# tcp 服务器地址和端口
target_server_type = 0  # 0 1002 wifi地址  1 1002网线地址   2 控制箱地址
if target_server_type == 0:
    server_ip = '192.168.199.222'
elif target_server_type == 1:
    server_ip = '192.168.9.19'
else:
    server_ip = '192.168.2.2'
server_port = 5566
# tcp_server_ip = utils.get_host_ip() # 自动获取ip
tcp_server_ip = server_ip
tcp_server_port = 5566
#1 qt tcp 2 tcp
tcp_server_type = 1
front_video_src = 'rtmp://rtmp01open.ys7.com:1935/v3/openlive/D50551834_1_2?expire=1657329096&id' \
                          '=335347591388602368&t=e1dd42835fd9bece1478d0d19d68b727dafbb8630d96a1272d65c3f389dd9bca&ev' \
                          '=100 '
back_video_src = 'rtmp://rtmp01open.ys7.com:1935/v3/openlive/F77671789_1_2?expire=1657506533&id' \
                 '=336091817970577408&t=d537867dd4f403d5b162f51e73011ee8f30670d6abac8d5dc6807f23ab98f6f6&ev' \
                 '=100 '
# front_video_src = r'F:\软件相关\开发软件\ffmpeg\bin\ffmpeg_test.flv'
# back_video_src = r'F:\软件相关\开发软件\ffmpeg\bin\ffmpeg_test.flv'