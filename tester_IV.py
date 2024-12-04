# 3rd - last step in program piramid
from tools import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing
hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Arm(Port.C, gears=[20, 28])
Ra = Arm(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)

#preparation
bot.set_origin(140, 110, 90, [[0,0],[2000, 1140]])
bot.align_wall_t(-100, 500)
bot.set_origin(145, 110, 90, [[0,0],[2000, 1140]])
La.align(-500)
La.reset_angle(0)
Ra.align(-500)
Ra.reset_angle(0)
bot.straight_g(20, 900)

#mission 1 clear the area
La.run_target(1000, 90, wait=False)
bot.straight_position(480, 585, 1)

La.run_target(1000, 230)
bot.straight_position(350, 500, -1)
print(bot.x, bot.y)
