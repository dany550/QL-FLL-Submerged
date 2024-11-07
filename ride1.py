from tools_II import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Motor(Port.C)
Ra = Motor(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(110, 155, 90, [[0,0],[2000, 1140]])
La.reset_angle(0)
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
bot.straight_position(-660, 805, 1)
bot.deaful_speed = 900
La.run_angle(1000, -140)
La.run_angle(1000, 140, wait = False)
bot.straight_g(-50)

#korál
bot.straight_position(-570, 840, 1)
La.run_angle(1000, -70, wait=False)
bot.straight_position(-340, -300, 1)
La.run_angle(1000, 20, wait=False)
bot.straight_g(70, set_angle=True)
La.run_angle(1000, -20, wait=False)
La.run_angle(1000, 70,wait=False)

#žralok
bot.straight_position(-400, -300, -1)
La.run_angle(1000, -100, wait=False)
bot.straight_g(180, 50, True, 45)
for i in range(2):    
    La.run_angle(1000, 120)
    La.run_angle(1000, -100)
La.run_angle(1000, -120)
bot.straight_g(-100)
La.run_target(1000, 0)

#druhej korál
#bot.straight_g(10, 50, True, 135)

#return
bot.straight_position(-200, 200,1)
bot.straight_position(1000, 400, 1, 900)
bot.straight_position(200, 400, 1)
bot.straight_position(110, 155, -1)
bot.turn(270, 0)

#bot.straight_position( -400, 700, 1, 900)
#bot.straight_position(-400, 300, 1)
#bot.straight_position(200, 300, -1, 900)
#bot.straight_position(110, 155, -1)




print(bot.x, bot.y)