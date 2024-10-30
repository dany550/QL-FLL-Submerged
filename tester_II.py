# 3rd - last step in program piramid
from tools_II import *
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(0,0,0)
timer = StopWatch()
time = 0
x = 0
y = 0
speed = Matrix([[0],[0],[0]])
while True:
    bot.get_orientation()
    acceleration = bot.hub.imu.acceleration()
    pasttime = time
    time = timer.time()
    timedif =  time - pasttime
    x = x + speed[1] * timedif/1000 + 0.5 * acceleration[1] * (timedif/1000) ** 2
    y = y + speed[0] * timedif/1000 + 0.5 * acceleration[0] * (timedif/1000) ** 2
    speed = acceleration * timedif/1000000 + speed

    print(time, x, y)