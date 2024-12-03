# 3rd - last step in program piramid
from tools import *
from pybricks.iodevices import XboxController
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(0,0,270)

remote = XboxController()

timer = StopWatch()
time = 0
x = 0
y = 0
speed = 0
acceleration = [0,0,0,0,0,0,0,0,0,0]

while True:
    pressed = remote.buttons.pressed()
    Ldir = remote.joystick_left()
    Rdir = remote.joystick_right()
    bot.Lw.run((Ldir[1]+Ldir[0])*10 + Rdir[1]+Rdir[0])
    bot.Rw.run((Ldir[1]-Ldir[0])*10 + Rdir[1]-Rdir[0])
    acceleration.append(abs(hub.imu.acceleration(Axis.Y)))
    acceleration.pop(0)
    suma = sum(acceleration)
    #if abs(acceleration) > abs(bot.Lw.speed()+bot.Rw.speed())*3+5000:
    #    hub.speaker.beep()
    if Button.A in pressed:
        print(suma)
    if Button.B in pressed:
        print()



field = [[0,0],[2000,1140]]
x = -51
y = 10
print(x,y)

if field[0][0] - field[1][0] != 0:
    x = (x - field[0][0]) % abs(field[0][0]- field[1][0]) + field[0][0]
if field[0][1] - field[1][1] != 0:
    y = (y - field[0][1]) % abs(field[0][1]- field[1][1]) + field[0][1]
print(x,y)

