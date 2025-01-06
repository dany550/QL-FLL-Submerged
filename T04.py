# 3rd - last step in program piramid
from tools import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing
hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
Cs = ColorSensor(Port.E)
Ra = Arm(Port.A)
bot = Robot(hub, 27.9, 158, Lw, Rw)

bot.set_origin(0,0,0)
bot.add_arms(Ra)

Ra.run_until_stalled(500)

