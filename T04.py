# 3rd - last step in program piramid
from T03 import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

bot.set_origin(0, 0, 0, [[0,0],[400, 400]])
for i in range(20):
    bot.straight_position(200, 100, 1)
    #print(bot.position())
    wait(500)
    bot.straight_position(100, 150, -1)
    #print(bot.position())
    wait(500)
    bot.straight_position(300, 0, 1)
    #print(bot.position())
    wait(500)
    bot.straight_position(0, 0, -1)
    print(bot.position())
    wait(500)

    #preparation
m20 = Setup(bot, 0, 0, 0, [[0,0],[310, 210]], 0, [-500])

#mission 1 clear the area
m21 = Mission(bot, 200, 100, 45, [20])
def m21_body():
    #print("m21", bot.position())
    La.target(100, 200)
    bot.turn(180, 50)
m21.add_body(m21_body)
m21.add_checkpoint(200, 100, 1)

m22 = Mission(bot, 300, 0, 180, [150])
def m22_body():
    #print("m22", bot.position())
    La.target(100, 200)
    bot.straight_g(50)
m22.add_body(m22_body)

m23 = Mission(bot, 100, 150, 0, [70])
def m23_body():
    #print("m23", bot.position())
    La.target(100, 200)
m23.add_body(m23_body)

m24 = Mission(bot, 0, 0, 0, [0])

#def ride
r2 = Ride(Color.YELLOW, m20, m21, m22, m23, m24)