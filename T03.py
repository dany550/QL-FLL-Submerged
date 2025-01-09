# 3rd - last step in program piramid
from F01_Tools import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
falcon = Robot(hub, 27.9, 158, Lw, Rw)
La = Arm(Port.D, falcon) #dflkadg
Cs = ColorSensor(Port.E)
falcon.add_arms(La)
falcon.extra_task = falcon.interupter
falcon.hub.system.set_stop_button(Button.BLUETOOTH)
bot = falcon