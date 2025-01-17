from M02_R01 import*
#from M02_R02 import*

rides = [r1]###########

color = Color.NONE
pressed = []
timer = StopWatch()
shake_speed = -500

while True:
    ppressed = pressed
    pressed = bot.hub.buttons.pressed()
    pcolor = color
    color = Cs.color()
    time = timer.time()
    bot.interupt = False
    
    if color != pcolor:
        if color != Color.NONE:
            hub.speaker.beep()
        else:
            hub.speaker.beep(400)

    if color == Color.NONE:
        for arm in bot.arms:
            arm.run(shake_speed)
    else:
        for arm in bot.arms:
            if arm.stalled():
                arm.stop()

    ride_n = 0
    for i in range(len(rides)):
        if color == rides[i].color:
            ride_n = i+1

    if ride_n != 0:
        ride_n -= 1
        bot.hub.light.on(Color.GREEN)
        bot.hub.display.pixel(0, 0, 0)
        bot.hub.display.pixel(ride_n//5 + 1, ride_n%5)

        for i in range(len(rides[ride_n].missions)):
            if rides[ride_n].missions[i].done:
                bot.hub.display.pixel(i//5 + 3, i%5, 50)
            else:
                bot.hub.display.pixel(i//5 + 3, i%5, 100)

        if Button.LEFT in pressed:
            for i in range(len(rides[ride_n].missions)):
                if not rides[ride_n].missions[i].done and i > 0:
                    rides[ride_n].missions[i-1].done = False
                    hub.speaker.beep(400)
                    break
                elif not rides[ride_n].missions[i].done and i == 0:
                    hub.speaker.beep(200)
                    break
                elif i == len(rides[ride_n].missions)-1:
                    rides[ride_n].missions[i].done = False
                    hub.speaker.beep(400)

        if Button.RIGHT in pressed:
            for i in range(len(rides[ride_n].missions)):
                if not rides[ride_n].missions[i].done and i < len(rides[ride_n].missions):
                    rides[ride_n].missions[i].done = True
                    hub.speaker.beep(400)
                    break
                elif i == len(rides[ride_n].missions)-1:
                    hub.speaker.beep(200)

        if Button.CENTER in pressed:
            bot.hub.light.on(Color.RED)
            bot.hub.display.pixel(0, 0, 0)
            bot.hub.display.pixel(0, 1, 0)
            bot.hub.display.pixel(0, 2, 100)
            hub.speaker.beep(600)
            for arm in bot.arms:
                arm.stop()
            rides[ride_n].setup.start()
            bot.locate()

            bot.hub.display.pixel(0, 2, 0)
            bot.hub.display.pixel(0, 3, 100)
            for mission_n in range(len(rides[ride_n].missions)):
                bot.hub.display.pixel(mission_n//5 + 3, mission_n%5, 50)
                hub.speaker.beep(800)
                rides[ride_n].missions[mission_n].start()
                if not bot.interupt:
                    rides[ride_n].missions[mission_n].done = True
                else:
                    break

        else:
            bot.hub.display.pixel(0, 1, 100)
            bot.hub.display.pixel(0, 2, 0)
            bot.hub.display.pixel(0, 3, 0)

    else:
        bot.hub.light.on(Color.YELLOW)
        bot.hub.display.pixel(0, 0, 100)
        bot.hub.display.pixel(0, 1, 0)
        bot.hub.display.pixel(0, 2, 0)
        bot.hub.display.pixel(0, 3, 0)

        for i in range(len(rides)):
            bot.hub.display.pixel(i//5 + 1, i%5, 50)
        for i in range(10):
            bot.hub.display.pixel(i//5 + 3, i%5, 0)
    
    wait(50)