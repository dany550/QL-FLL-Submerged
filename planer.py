# 3rd - last step in program piramid
# this file has a great potential (code generator, 3 moods)
from F01_Tools import *
from pybricks.iodevices import XboxController
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")


hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
La = Arm(Port.C, bot, gears=[20, 28]) #dflkadg
Ra = Arm(Port.D, bot)
bot.set_origin(0, 0, 0)

remote = XboxController()

speed = 0
motor = 0

while True:
    bot.locate()
    pressed = remote.buttons.pressed()
    Ldir = remote.joystick_left()
    Rdir = remote.joystick_right()
    trigers = remote.triggers()
    bot.Lw.run((Ldir[1]+Ldir[0])*10 + Rdir[1]+Rdir[0])
    bot.Rw.run((Ldir[1]-Ldir[0])*10 + Rdir[1]-Rdir[0])
    acceleration = hub.imu.acceleration(Axis.X)
    if abs(acceleration) > abs(bot.Lw.speed()+bot.Rw.speed())*3+5000:
        hub.speaker.beep()
    
    if Button.A in pressed:
        print(bot.x, bot.y)
    if Button.X in pressed:
        bot.set_origin(0, 0, bot.orientation)
    if Button.LB in pressed:
        motor = 0
    if Button.RB in pressed:
        motor = 1
    if motor == 0:
        La.run((trigers[0]-trigers[1])*10)
    if motor == 1:
        Ra.run((trigers[0]-trigers[1])*10)

    



field = [[0,0],[2000,1140]]
x = -51
y = 10
print(x,y)

if field[0][0] - field[1][0] != 0:
    x = (x - field[0][0]) % abs(field[0][0]- field[1][0]) + field[0][0]
if field[0][1] - field[1][1] != 0:
    y = (y - field[0][1]) % abs(field[0][1]- field[1][1]) + field[0][1]
print(x,y)