# 3rd - last step in program piramid
from T03 import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
La = Arm(Port.C, bot, gears=[20, 28]) #dflkadg
Ra = Arm(Port.D, bot)
Cs = ColorSensor(Port.F)
Ul = Ultrasonic(Port.E, )
bot.add_arms(La, Ra)
bot.extra_task = bot.interupter
bot.hub.system.set_stop_button(Button.BLUETOOTH)