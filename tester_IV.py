# 3rd - last step in program piramid
from tools import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing
hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
arm = Arm(Port.A)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.add_arms(arm)
bot.set_origin(0,0,0)
m1 = Mission(bot, 100, 100, 0, [90])
m1.start()

