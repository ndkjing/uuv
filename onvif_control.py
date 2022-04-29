from onvif import ONVIFCamera
import zeep
import time
import requests
from requests.auth import HTTPDigestAuth


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


class Onvif_hik(object):
    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue
        self.save_path = "./{}T{}.jpg".format(self.ip, str(time.time()))  # 截图保存路径

    def content_cam(self):
        """
        链接相机地址
        :return:
        """
        try:
            self.mycam = ONVIFCamera(self.ip, 80, self.username, self.password)
            self.media = self.mycam.create_media_service()  # 创建媒体服务
            self.media_profile = self.media.GetProfiles()[0]  # 获取配置信息
            self.imaging = self.mycam.create_imaging_service()
            self.ptz = self.mycam.create_ptz_service()  # 创建控制台服务
            # self.profile = self.mycam.media.GetProfiles()[0]
            # print(self.media_profile.token)
            # params = self.ptz.create_type('GetStatus')
            # params.ProfileToken = self.media_profile.token
            # res = self.ptz.GetStatus(params)
            # print('res',res)
            print('##########################连接成功')
            return True
        except Exception as e:
            print('##########################连接失败',e)
            return False

    def Snapshot(self):
        """
        截图
        :return:
        """
        res = self.media.GetSnapshotUri({'ProfileToken': self.media_profile.token})
        response = requests.get(res.Uri, auth=HTTPDigestAuth(self.username, self.password))
        with open(self.save_path, 'wb') as f:  # 保存截图
            f.write(response.content)

    def get_presets(self):
        """
        获取预置点列表
        :return:预置点列表--所有的预置点
        """
        presets = self.ptz.GetPresets({'ProfileToken': self.media_profile.token})  # 获取所有预置点,返回值：list
        return presets

    def goto_preset(self, presets_token: int):
        """
        移动到指定预置点
        :param presets_token: 目的位置的token，获取预置点返回值中
        :return:
        """
        try:
            self.ptz.GotoPreset(
                {'ProfileToken': self.media_profile.token, "PresetToken": presets_token})  # 移动到指定预置点位置
        except Exception as e:
            print(e)

    def zoom(self, zoom: float=0.1, timeout: float = 0.1):
        """
        变倍
        :param zoom: 拉近或远离  浮点数 负数拉近  正数拉远  [-1,1]
        :param timeout: 生效时间
        :return:
        """
        request = self.ptz.create_type('ContinuousMove')
        request.ProfileToken = self.media_profile.token
        request.Velocity = {"Zoom": zoom}
        self.ptz.ContinuousMove(request)
        time.sleep(timeout)
        self.ptz.Stop({'ProfileToken': request.ProfileToken})

    def continue_move_image(self, speed=1.0):
        """
        # 焦距持续移动 正数聚焦远处  负数聚焦近处
        :param speed: [-1,1]
        :return:
        """
        request1 = self.imaging.create_type('Move')
        request1.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        request1.Focus = {'Continuous': {'Speed': speed}}
        self.imaging.Move(request1)
        time.sleep(0.2)
        # self.imaging.Stop.VideoSourceToken= self.media_profile.VideoSourceConfiguration.SourceToken
        # self.imaging.Stop({'VideoSourceToken': self.media_profile.VideoSourceConfiguration.SourceToken})
        # 调节一段时间后立即停止来控制焦距运动
        request2 = self.imaging.create_type('Stop')
        request2.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        # request2.Focus = {'Continuous': {'Speed': -0}}
        self.imaging.Stop(request2)
        # print('req 2')
        # time.sleep(0.1)
        # self.imaging.Stop()

    def relative_move_image(self, dist, speed=1.0):
        # 焦距相对移动
        request = self.imaging.create_type('Move')
        print('d',dist,type(dist))
        request.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        request.Focus = {'Relative': {'Distance': dist, 'Speed': speed}}
        # request.Focus = {'Relative': {'Distance': (dist)}}
        self.imaging.Move(request)

    def absolute_move_image(self, dist, speed=0.1):
        # 焦距相对移动
        request = self.imaging.create_type('Move')
        print('d',dist,type(dist))
        request.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        request.Focus = {'Absolute':{'Position':dist}}
        self.imaging.Move(request)

    def set_imaging(self,Brightness=50):
        requestGetImaging = self.imaging.create_type('GetImagingSettings')
        video_sources = self.media.GetVideoSources()
        requestGetImaging.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        responseGetImageSettings = self.imaging.GetImagingSettings(requestGetImaging)
        requestSetImaging = self.imaging.create_type('SetImagingSettings')
        requestSetImaging.VideoSourceToken = self.media_profile.VideoSourceConfiguration.SourceToken
        requestSetImaging.ImagingSettings = responseGetImageSettings
        requestSetImaging.ImagingSettings.Brightness = Brightness  # 1-99
        # requestSetImaging.ImagingSettings.Focus = "AutoFocusMode"
    #     {
    #     'AutoFocusMode': 'AutoFocusMode'
    # }  #
        self.imaging.SetImagingSettings(requestSetImaging)


if __name__ == '__main__':
    obj = Onvif_hik('192.168.1.168', 'admin', 'xxl123456')
    print(obj.content_cam())
    while 1:
        a=input("zoom:")
        # obj.set_imaging()
        # obj.zoom(float(a),0.2)
        obj.continue_move_image(float(a))
        # obj.relative_move_image(float(a))
        # obj.absolute_move_image(float(a))

