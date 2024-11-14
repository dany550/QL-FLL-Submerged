# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw,)
bot.set_origin(0,0,0)
print(bot.x, bot.y, bot.avr_motor_angle, bot.Lw.angle(), bot.Rw.angle())

bot.align_wall_a(500)
