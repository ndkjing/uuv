import os
import utils

root_path = os.path.dirname(os.path.abspath(__file__))
print('root_path', root_path)
save_dir = os.path.join(root_path, 'statics')
save_imgs_dir = os.path.join(save_dir, 'imgs')
save_videos_dir = os.path.join(save_dir, 'videos')
save_pid_path = os.path.join(save_dir, 'pid.json')  # 保存pid设置路径
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
if not os.path.exists(save_imgs_dir):
    os.mkdir(save_imgs_dir)
if not os.path.exists(save_videos_dir):
    os.mkdir(save_videos_dir)
tcp_server_ip = utils.get_host_ip()
tcp_server_port = 9002
