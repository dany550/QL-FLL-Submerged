# 3rd - last step in program piramid
from tools import *
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

x1 = 0
x2 = 0
y1 = 0
y2 = 300
ori1 = -1
ori2 = 0

x_shift = x2 - x1
y_shift = y2 - y1
track_angle = angle_mod(degrees(atan2(y_shift, x_shift)))
ori_diff = abs(angle_mod(track_angle - ori1) + angle_mod(track_angle - ori2))
direction = sign(180 - ori_diff, False)
track_angle = track_angle * direction
distance = sqrt(x_shift**2 + y_shift**2)*direction
print(track_angle, distance)