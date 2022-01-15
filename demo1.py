# created by Huang Lu
# 27/08/2016 17:24:55
# Department of EE, Tsinghua Univ.

import cv2
import numpy as np
import config
# cap = cv2.VideoCapture(config.front_video_src)
cap = cv2.VideoCapture("rtmp://116.62.44.118:1935/live/index")
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("http://116.62.44.118:8081/live/index.m3u8")
# cap = cv2.VideoCapture("http://116.62.44.118:8081/live/index.flv")
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    print(frame.shape)
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
