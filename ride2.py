from tools import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Motor(Port.C)
Ra = Motor(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(2000 - 148, 159, 90, [[0,0],[2000, 1140]])

bot.straight_position()
