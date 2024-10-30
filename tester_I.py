# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing


hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(0,0,270)
#bot.straight_g(100, set_angle=True, angle=270)
#bot.turn(90, 0)
bot.straight_position(0, 100, 1)

print(hub.imu.heading())
wait(1000)
print(hub.imu.heading())


field = [[0,0],[2000,1140]]
x = -51
y = 10
print(x,y)

if field[0][0] - field[1][0] != 0:
    x = (x - field[0][0]) % abs(field[0][0]- field[1][0]) + field[0][0]
if field[0][1] - field[1][1] != 0:
    y = (y - field[0][1]) % abs(field[0][1]- field[1][1]) + field[0][1]
print(x,y)