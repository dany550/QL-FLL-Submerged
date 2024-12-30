from tools import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Arm(Port.C, gears=[20, 28])
Ra = Arm(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.add_arms(La, Ra)