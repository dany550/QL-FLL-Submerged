# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
arm = Motor(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw,)
bot.set_origin(0,0,0)
print(bot.x, bot.y, bot.avr_motor_angle, bot.Lw.angle(), bot.Rw.angle())

#bot.turn(-360,-bot.onerot/2)
#print(bot.x, bot.y, bot.avr_motor_angle, Lw.angle(), Rw.angle())
arm.run_target(100, 0)

bot.turn(370, 70)

bot.get_orientation()
print("!1",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())

bot.orientation_dif += 360
arm.run_target(100, 20)

bot.get_orientation()
print("!2",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())

bot.straight_position(0, 20, 1)
bot.turn(0,0)
bot.turn(-30, 50)
arm.run_target(100, 0)
corner = [bot.x, bot.y]
bot.turn(-150, 50)
bot.straight_position(corner[0], corner[1], 1)
arm.run_target(100, 20)

bot.get_orientation()
print("!pusa",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())

bot.straight_position(30, 50, 1)
bot.get_orientation()
print("!3",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())

arm.run_target(100, 0)
bot.straight_g(-30, set_angle=True, angle = 0)
arm.run_target(100, 20)
bot.get_orientation()
print("!4",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())
bot.straight_position(30, 90, 1)
bot.get_orientation()
print("!5",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())

arm.run_target(100, 0)
bot.straight_g(-30, set_angle=True, angle = 0)
arm.run_target(100, 20)
bot.straight_position(200, 200, 1)
bot.get_orientation()
print(bot.x, bot.y, bot.orientation(), bot.Lw.angle(), bot.Rw.angle())