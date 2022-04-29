# -*- coding: utf-8 -*-
import math
import numpy as np
from numpy import *

# 计算两圆交点
def insec(p1, r1, p2, r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
    if d > (R + S) or d < (abs(R - S)):
        print("Two circles have no intersection")
        return
    elif d == 0 and R == S:
        print("Two circles have same center!")
        return
    else:
        A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(R ** 2 - A ** 2)
        x2 = x + A * (a - x) / d
        y2 = y + A * (b - y) / d
        x3 = round(x2 - h * (b - y) / d, 2)
        y3 = round(y2 + h * (a - x) / d, 2)
        x4 = round(x2 + h * (b - y) / d, 2)
        y4 = round(y2 - h * (a - x) / d, 2)
        print(x3, y3)
        print(x4, y4)
        c1 = np.array([x3, y3])
        c2 = np.array([x4, y4])
        return c1, c2

def circle_points():
    P1 = np.array([-5, 0])
    R1 = 10
    P2 = np.array([5, 0])
    R2 = 5
    C = insec(P1, R1, P2, R2)
    C1 = C[0]
    C2 = C[1]

# 计算三球交点
def main_GPSLocation(info_list):
    i = 1
    j = 0
    k=0
    c = 0.299792458  # 光速 0.299792458km/us
    x = zeros((6, 4)) #存储6个卫星的（x,y,z,t）参数
    while i<=6:
        # print(" %s %d" % ("please input (x,y,z,t) of group",i) )
        # temp=input()
        temp=info_list[k]
        x[i-1]=temp.split()
        while j<4:
            x[i-1][j]=float(x[i-1][j])
            j=j+1
        i=i+1
        k+=1
    a=zeros((4,4)) #系数矩阵
    b=zeros((4,1)) #常数项
    j=0
    while j<4:
        a[j][0]=2*(x[5][0]-x[j][0])
        a[j][1]=2*(x[5][1]-x[j][1])
        a[j][2]=2*(x[5][2]-x[j][2])
        a[j][3]=2*c*c*(x[j][3]-x[5][3])
        b[j][0]=x[5][0] * x[5][0] - x[j][0] * x[j][0] + \
                x[5][1] * x[5][1] - x[j][1] * x[j][1] + \
                x[5][2] * x[5][2] - x[j][2] * x[j][2] + \
            c*c*(x[j][3] * x[j][3] - x[5][3] * x[5][3])
        j=j+1
    a_ni=linalg.inv(a) #系数矩阵求逆
    print(dot(a_ni,b))


if __name__ == '__main__':
    main_GPSLocation(['3 2 3 10010.00692286', '1 3 1 10013.34256381', '5 7 4 10016.67820476', '1 7 3 10020.01384571',
                      '7 6 7 10023.34948666', '1 4 9 10030.02076857'])
