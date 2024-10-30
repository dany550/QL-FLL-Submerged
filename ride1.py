from tools_II import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Motor(Port.C)
Ra = Motor(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(110, 155, 90, [[0,0],[2000, 1140]])
bot.straight_g(20, 900)

#chobotnice
bot.straight_position(500, 500, 1, 900)
bot.straight_g(70, set_angle=True, angle=45)
bot.straight_g(-150,set_angle=True, angle=45)

#ryba
bot.straight_position(600, 450, 1, 900)
bot.straight_position(930, 680, 1, 900)
bot.straight_g(200, 50, True, 45)

#loď
bot.deaful_speed = 400
bot.straight_position(-660, 810, 1)
bot.deaful_speed = 900
La.run_angle(1000, -140)
La.run_angle(1000, 140, wait = False)
bot.straight_g(-50)

#korál
bot.straight_position(-580, 880, 1, 900)
bot.straight_position()

#bot.straight_position( -400, 700, 1, 900)
#bot.straight_position(-400, 300, 1)
#bot.straight_position(200, 300, -1, 900)
#bot.straight_position(110, 155, -1)




print(bot.x, bot.y)