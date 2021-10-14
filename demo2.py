import cv2
import numpy as np
import math
import datetime

# 初始化一个空画布 300×300 三通道 背景色为白色
margin = 30  # 上下左右边距
size_w = 300
radius = int((size_w - 2 * margin) / 2)  # 圆的半径
center = (center_x, center_y) = (int(radius + margin), int(radius + margin))  # 圆心

img = np.ones((size_w, size_w, 3), dtype="uint8")
# img *= 255  # 白色底
# 蓝色底
rgb = [153, 194, 255]
img[:, :, 0] = np.squeeze(np.ones((size_w, size_w, 1), dtype="uint8") * rgb[2])
img[:, :, 1] = np.squeeze(np.ones((size_w, size_w, 1), dtype="uint8") * rgb[1])
img[:, :, 2] = np.squeeze(np.ones((size_w, size_w, 1), dtype="uint8") * rgb[0])

# 绘制一个绿色的圆
cv2.circle(img, center=center, radius=radius, color=(0, 255, 0), thickness=1)
pt1 = []

# 3. 画出60条秒和分钟的刻线
for i in range(60):
    # 最外部圆，计算A点
    x1 = center_x + (radius - 5) * math.cos(i * 6 * np.pi / 180.0)
    y1 = center_y + (radius - 5) * math.sin(i * 6 * np.pi / 180.0)
    pt1.append((int(x1), int(y1)))

    # 同心小圆，计算B点
    x2 = center_x + (radius - margin) * math.cos(i * 6 * np.pi / 180.0)
    y2 = center_y + (radius - margin) * math.sin(i * 6 * np.pi / 180.0)

    cv2.line(img, pt1[i], (int(x2), int(y2)), (0, 0, 0), thickness=1)

# 4. 画出12条小时的刻线
for i in range(12):
    # 12条小时刻线应该更长一点
    x = center_x + (radius - int(margin * 1.5)) * math.cos(i * 30 * np.pi / 180.0)
    y = center_y + (radius - int(margin * 1.5)) * math.sin(i * 30 * np.pi / 180.0)
    # 这里用到了前面的pt1
    cv2.line(img, pt1[i * 5], (int(x), int(y)), (0, 0, 0), thickness=2)

# 5 绘制 角度 绘制文字
for i in range(12):
    # 12条小时刻线应该更长一点
    if 0 <= i <= 3 or 9 <= i < 12:
        delta_margin = int(margin / 3)
    else:
        delta_margin = int(margin * 4 / 5)
    x = center_x + (radius + delta_margin) * math.cos(i * 30 * np.pi / 180.0)
    y = center_y + (radius + delta_margin) * math.sin(i * 30 * np.pi / 180.0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    show_angle = str((i * 30 + 90) % 360)
    # show_angle = str(i * 30)
    cv2.putText(img, show_angle, (int(x), int(y)), font, 0.4, (0, 0, 0), 1)
    show_n = False
    if i == 0:
        show_n = True
        str_n = 'E'
    elif i == 3:
        show_n = True
        str_n = 'S'
    elif i == 6:
        show_n = True
        str_n = 'W'
    elif i == 9:
        show_n = True
        str_n = 'N'
    else:
        show_n = False
        str_n = ''
    if show_n:
        x_n = center_x + (radius - int(margin * 2)) * math.cos(i * 30 * np.pi / 180.0)
        y_n = center_y + (radius - int(margin * 2)) * math.sin(i * 30 * np.pi / 180.0)
        cv2.putText(img, str_n, (int(x_n), int(y_n)), font, 1, (0, 0, 0), 1)


# 6 绘制角度线
def angle(angle_z=80):
    angle_z = angle_z - 90
    if angle_z < 0:
        angle_z = angle_z + 360
    x = center_x + (radius - margin * 2) * math.cos(angle_z * np.pi / 180.0)
    y = center_y + (radius - margin * 2) * math.sin(angle_z * np.pi / 180.0)
    # 这里用到了前面的pt1
    cv2.line(img, center, (int(x), int(y)), (0, 0, 255), thickness=3)
    # # 绘制箭头
    # if i==0:
    #     x_0 = center_x + (radius + delta_margin) * math.cos(i * 30 * np.pi / 180.0)
    #     y_0 = center_y + (radius + delta_margin) * math.sin(i * 30 * np.pi / 180.0)
    #     points =
    #     cv2.polylines(img=img, pts=[points], isClosed=True, color=(0, 0, 255), thickness=3)


# 绘制角度线
angle(330)
cv2.imshow("circle", img)

cv2.imwrite("draw_circle.png", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
