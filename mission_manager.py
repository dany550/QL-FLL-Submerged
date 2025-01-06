from tools import*

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
Cs = ColorSensor(Port.E)
Ra = Arm(Port.A)
bot = Robot(hub, 27.9, 158, Lw, Rw)
bot.extra_task = bot.interupter
bot.add_arms(Ra)
bot.hub.system.set_stop_button(Button.BLUETOOTH)

# mission definitions
m11 = Mission(bot, 100, 100, 15, [50])
def m11_body():
    bot.straight_g(100)
    Ra.run_target(1000, 500)
    bot.straight_g(-100)
m11.add_body(m11_body)

m12 = Mission(bot, 500, 0, -50, [200])
def m12_body():
    bot.turn(50, 500)
    Ra.run_target(500, 500) #danger interupter ###
m12.add_body(m12_body)

### ride definitions
r1 = Ride(bot, 0, 0, 0, [[0,0],[2000, 1140]], -500, [200], m11, m12)
r2 = Ride(bot, 0, 0, 0, [[0,0],[2000, 1140]], -500, [200], m11, m12, m11)
r3 = Ride(bot, 0, 0, 0, [[0,0],[2000, 1140]], -500, [200], m11, m12, m11, m11, m11, m11, m11, m11, m11, m11, m11)
rides = [r1, r2, r3]

color = Color.NONE
timer = StopWatch()
shake_speed = 500


while True:
    pressed = bot.hub.buttons.pressed()
    pcolor = color
    color = Cs.color()
    time = timer.time()
    
    if color != pcolor:
        if color != Color.NONE:
            hub.speaker.beep()
        else:
            hub.speaker.beep(400)

    for arm in bot.arms:
        arm.run(shake_speed) # might be upgraded with arm_setup

    if color == Color.YELLOW:
        ride_n = 1
    elif color == Color.BLUE:
        ride_n = 2
    elif color == Color.RED:
        ride_n = 3
    else:
        ride_n = 0

    if ride_n != 0:
        ride_n -= 1
        bot.hub.light.on(Color.GREEN)
        bot.hub.display.pixel(0, 0, 0)
        bot.hub.display.pixel(ride_n//5 + 1, ride_n%5)

        for i in range(len(rides[ride_n].missions)):
            if rides[ride_n].missions[i].done:
                bot.hub.display.pixel(i//5 + 3, i%5)
            else:
                bot.hub.display.pixel(i//5 + 3, i%5, 50)

        if Button.CENTER in pressed:
            bot.hub.light.on(Color.RED)
            bot.hub.display.pixel(0, 0, 0)
            bot.hub.display.pixel(0, 1, 0)
            bot.hub.display.pixel(0, 2, 100)
            hub.speaker.beep(600)
            for arm in bot.arms:
                arm.stop()
            rides[ride_n].setup()

            bot.hub.display.pixel(0, 2, 0)
            bot.hub.display.pixel(0, 3, 100)
            for mission_n in range(len(rides[ride_n].missions)):
                bot.hub.display.pixel(mission_n//5 + 3, mission_n%5)
                hub.speaker.beep(800)
                rides[ride_n].missions[mission_n].start()
                if not bot.interupt:
                    rides[ride_n].missions[mission_n].done = True

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


    
#to upgrade
    #make all functions interuptable
    #progress restarter and mission menu
    #automatic directions
    #automatic arm stoper and ride starter
    #advanced checkpoints