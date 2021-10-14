import cv2
import numpy as np
import math
import config

class DrawAngle:
    def __init__(self, margin_=30, size_w_=300):
        # 初始化一个空画布 300×300 三通道 背景色为白色
        self.margin = margin_  # 上下左右边距
        self.size_w = size_w_
        self.radius = int((self.size_w - 2 * self.margin) / 2)  # 圆的半径
        (self.center_x, self.center_y) = (int(self.radius + self.margin), int(self.radius + self.margin))  # 圆心
        self.center = (self.center_x, self.center_y)


    def draw_y(self, angle_y=80,b_show=False):
        """
        绘制横滚图
        :return:
        """
        img = np.ones((self.size_w, self.size_w, 3), dtype="uint8")
        # img *= 255
        # 蓝色底
        rgb = [153, 194, 255]
        img[:, :, 0] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[2])
        img[:, :, 1] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[1])
        img[:, :, 2] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[0])
        # 绘制一个绿色的圆
        cv2.circle(img, center=self.center, radius=self.radius, color=(255, 0, 0), thickness=1)
        # 绘制两条垂直辅助线
        cv2.line(img, (int(self.center_x - self.radius), int(self.center_y)),
                 (int(self.center_x + self.radius), int(self.center_y)), (128, 128, 128),
                 thickness=1)
        cv2.line(img, (int(self.center_x), int(self.center_y - self.radius)),
                 (int(self.center_x), int(self.center_y + self.radius)), (128, 128, 128),
                 thickness=1)

        # 绘制角度线
        x_0 = self.center_x - (self.radius - self.margin) * math.cos(angle_y * np.pi / 180.0)
        y_0 = self.center_y - (self.radius - self.margin) * math.sin(angle_y * np.pi / 180.0)
        x_1 = self.center_x + (self.radius - self.margin) * math.cos(angle_y * np.pi / 180.0)
        y_1 = self.center_y + (self.radius - self.margin) * math.sin(angle_y * np.pi / 180.0)
        cv2.line(img, (int(x_0), int(y_0)), (int(x_1), int(y_1)), (0, 255, 0), thickness=3)

        # 绘制角度线
        cv2.imwrite(config.save_angle_y_path, img)
        if b_show:
            cv2.imshow("circle", img)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def draw_z(self,angle_z,b_show=False):
        img = np.ones((self.size_w, self.size_w, 3), dtype="uint8")
        # img *= 255
        # 蓝色底
        rgb = [153, 194, 255]
        img[:, :, 0] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[2])
        img[:, :, 1] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[1])
        img[:, :, 2] = np.squeeze(np.ones((self.size_w, self.size_w, 1), dtype="uint8") * rgb[0])
        # 绘制一个绿色的圆
        cv2.circle(img, center=self.center, radius=self.radius, color=(0, 255, 0), thickness=1)
        pt1 = []

        # 3. 画出60条秒和分钟的刻线
        for i in range(60):
            # 最外部圆，计算A点
            x1 = self.center_x + (self.radius - 5) * math.cos(i * 6 * np.pi / 180.0)
            y1 = self.center_y + (self.radius - 5) * math.sin(i * 6 * np.pi / 180.0)
            pt1.append((int(x1), int(y1)))

            # 同心小圆，计算B点
            x2 = self.center_x + (self.radius - self.margin) * math.cos(i * 6 * np.pi / 180.0)
            y2 = self.center_y + (self.radius - self.margin) * math.sin(i * 6 * np.pi / 180.0)

            cv2.line(img, pt1[i], (int(x2), int(y2)), (0, 0, 0), thickness=1)

        # 4. 画出12条小时的刻线
        for i in range(12):
            # 12条小时刻线应该更长一点
            x = self.center_x + (self.radius - int(self.margin * 1.5)) * math.cos(i * 30 * np.pi / 180.0)
            y = self.center_y + (self.radius - int(self.margin * 1.5)) * math.sin(i * 30 * np.pi / 180.0)
            # 这里用到了前面的pt1
            cv2.line(img, pt1[i * 5], (int(x), int(y)), (0, 0, 0), thickness=2)

        # 5 绘制 角度 绘制文字
        for i in range(12):
            # 12条小时刻线应该更长一点
            if 0 <= i <= 3 or 9 <= i < 12:
                delta_margin = int(self.margin / 3)
            else:
                delta_margin = int(self.margin * 4 / 5)
            x = self.center_x + (self.radius + delta_margin) * math.cos(i * 30 * np.pi / 180.0)
            y = self.center_y + (self.radius + delta_margin) * math.sin(i * 30 * np.pi / 180.0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            show_angle = str((i * 30 + 90) % 360)
            # show_angle = str(i * 30)
            cv2.putText(img, show_angle, (int(x), int(y)), font, 0.3, (0, 0, 0), 1)
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
                x_n = self.center_x + (self.radius - int(self.margin * 2)) * math.cos(i * 30 * np.pi / 180.0)
                y_n = self.center_y + (self.radius - int(self.margin * 2)) * math.sin(i * 30 * np.pi / 180.0)
                cv2.putText(img, str_n, (int(x_n), int(y_n)), font, 0.7, (0, 0, 0), 1)

        # 6 绘制角度线
        angle_z = angle_z - 90
        if angle_z < 0:
            angle_z = angle_z + 360
        x = self.center_x + (self.radius - self.margin * 2) * math.cos(angle_z * np.pi / 180.0)
        y = self.center_y + (self.radius - self.margin * 2) * math.sin(angle_z * np.pi / 180.0)
        # 这里用到了前面的pt1
        cv2.line(img, self.center, (int(x), int(y)), (0, 0, 255), thickness=3)
        # # 绘制箭头
        # if i==0:
        #     x_0 = center_x + (radius + delta_margin) * math.cos(i * 30 * np.pi / 180.0)
        #     y_0 = center_y + (radius + delta_margin) * math.sin(i * 30 * np.pi / 180.0)
        #     points =
        #     cv2.polylines(img=img, pts=[points], isClosed=True, color=(0, 0, 255), thickness=3)

        # 绘制角度线
        cv2.imwrite(config.save_angle_z_path, img)
        if b_show:
            cv2.imshow("circle", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    draw_angle_obj = DrawAngle(20,200)
    draw_angle_obj.draw_y(20,b_show=True)
    draw_angle_obj.draw_z(30,b_show=True)
