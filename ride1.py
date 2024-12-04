from tools import *

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
bot.straight_position(300, 520, -1)
bot.straight_position(400, 860, 1)

#mission 2 coral
Ra.run_target(1000, 720, wait=False)
La.run_target(1000, 120, wait=False)
bot.straight_position(430, 800, -1)

bot.straight_g(70, 50, True, 180)
La.run_target(1000, 95, wait=False)
bot.straight_g(50)
La.run_target(1000, 140)
bot.straight_g(20)
Ra.run_angle(1000, 500)
bot.straight_g(-100)

#mission 3 shark
La.run_target(1000, 100, wait=False)
Ra.run_target(1000, 1300, wait=False)
bot.straight_position(320, -220, 1)
bot.turn(135, 0)
bot.straight_g(30)
La.run_target(1000, 20)
bot.straight_g(-150)

#mission 4 reef
La.run_target(1000, 160, wait=False)
Ra.run_target(1000, 1300, wait=False)
bot.straight_position(360, 960, 1)
bot.turn(25, 0)
bot.straight_g(35)
La.run_target(1000, 100)
bot.straight_g(-50)
bot.turn(70, 0, 500, speed=500)
Ra.run_target(500, 900, wait=False)
bot.straight_position(470, 800, -1)
bot.turn(90, 0)
bot.straight_g(50)
Ra.run_target(500, 720)
bot.straight_g(-100)