# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.set_origin(0,0,0)
hub.system.set_stop_button(Button.BLUETOOTH)
print(bot.x, bot.y, bot.avr_motor_angle, bot.Lw.angle(), bot.Rw.angle())

def interupt():
    pressed = hub.buttons.pressed()
    if Button.CENTER in pressed:
        bot.interupt = True
bot.extra_task=interupt

missions = [1,2,3,4]
while missions:
    mission = missions[0]
    if bot.interupt:
        wait(10000)
        bot.interupt=False
    elif 1 in missions:
        bot.straight_position(100, 100, 1)
        wait(1000)
        bot.hub.speaker.beep()
        if not bot.interupt:
            missions.remove(1)

    elif 2 in missions:
        bot.straight_position(100, -100, 1)
        wait(1000)
        bot.hub.speaker.beep()
        if not bot.interupt:
            missions.remove(2)

    elif 3 in missions:
        bot.straight_position(-100, -100, 1)
        wait(1000)
        bot.hub.speaker.beep()
        if not bot.interupt:
            missions.remove(3)

    elif 4 in missions:
        bot.straight_position(-100, 100, 1)
        wait(1000)
        bot.hub.speaker.beep()
        if not bot.interupt:
            missions.remove(4)

bot.gandalf()
