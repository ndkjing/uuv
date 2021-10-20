import cv2
import datetime

import os
command_sonar1 = "D:\\apps\pingviewer_release\deploy\pingviewer.exe"
command_sonar2 = "D:\pingviewer_release\deploy\pingviewer.exe"
command_sonar3 = "F:\\apps\pingviewer_release\deploy\pingviewer.exe"
if os.path.exists(command_sonar1):
    r_v = os.system(command_sonar1)
if os.path.exists(command_sonar2):
    r_v = os.system(command_sonar2)
if os.path.exists(command_sonar3):
    r_v = os.system(command_sonar3)