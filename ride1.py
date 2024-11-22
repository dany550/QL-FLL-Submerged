from tools_II import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Arm(Port.C, gears=[20, 28])
Ra = Arm(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)

#preparation
bot.set_origin(140, 110, 90, [[0,0],[2000, 1140]])
bot.align_wall_t(-100, 500)
bot.set_origin(140, 110, 90, [[0,0],[2000, 1140]])
La.align(-500)
La.reset_angle(0)
bot.straight_g(20, 900)

#mission 1 clear the area
La.run_target(1000, 90, wait=False)
bot.straight_position(460 ,520, 1)
bot.straight_g(60, 50, True, 50)
La.run_target(1000, 210)
