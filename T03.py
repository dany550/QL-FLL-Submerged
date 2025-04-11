# 3rd - last step in program piramid
from F01_Tools import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
falcon = Robot(hub, 27.9, 158, Lw, Rw)
bot = falcon
while True:
    bot.gandalf()