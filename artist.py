# based on code version 2.0.1 on 26th Sept. 2024
from pybricks.iodevices import XboxController
from tools_II import*

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
arm = Motor(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw,)
bot.hub.system.set_stop_button(Button.BLUETOOTH)

def draw(on):
    if on:
        arm.run_target(100, 0)
    else:
        arm.run_target(100, 20)

def emogi():
    bot.set_origin(0,0,0)
    draw(True)
    bot.turn(370, 70)
    bot.orientation_dif += 360
    draw(False)
    bot.straight_position(0, 20, 1)
    bot.turn(0,0)
    bot.turn(-30, 50)
    draw(True)
    corner = [bot.x, bot.y]
    bot.turn(-150, 50)
    bot.straight_position(corner[0], corner[1], 1)
    draw(False)
    bot.straight_position(30, 50, 1)
    bot.turn(0, 0)
    draw(True)
    bot.straight_g(-30, set_angle=True, angle = 0)
    draw(False)
    bot.straight_position(30, 90, 1)
    bot.turn(0, 0)
    draw(True)
    bot.straight_g(-30, set_angle=True, angle = 0)
    draw(False)

Flower = Matrix(
    [
        [0, 50, 100, 50, 0],
        [0, 100, 0, 100, 0],
        [0, 50, 100, 50, 0],
        [0, 0, 100, 0, 0],
        [0, 100, 100, 100, 0],
    ]
)

def flower(r):
    bot.set_origin(0,0,0)
    draw(True)
    for petal in range(20):
        #bot.turn(petal * 18, 0)
        bot.straight_g(r, set_angle=True, angle=petal*18)
        bot.straight_g(-r)
    bot.straight_g(r*2)
    bottom = [bot.x, bot.y]
    bot.orientation_dif += 360
    bot.turn(110, 0)
    bot.turn(155, 2*r)
    bot.straight_position(bottom[0], bottom[1], -1)
    bot.turn(70, 0)
    bot.turn(25, 2*r)
    bot.straight_position(bottom[0], bottom[1], 1)

Fflower = Matrix(
    [
        [0, 0, 100, 0, 0],
        [0, 100, 100, 100, 0],
        [0, 0, 100, 0, 0],
        [0, 0, 100, 0, 0],
        [0, 100, 100, 100, 0],
    ]
)

def fflower(r):
    bot.set_origin(0,0,0)
    draw(True)
    for petal in range(20):
        #bot.turn(petal * 18, 0)
        bot.straight_g(r, set_angle=True, angle=petal*18)
        bot.straight_position(0,0,-1)
    bot.straight_g(r*2)
    bottom = [bot.x, bot.y]
    bot.orientation_dif += 360
    bot.turn(110, 0)
    bot.turn(155, 2*r)
    bot.straight_position(bottom[0], bottom[1], -1)
    bot.turn(70, 0)
    bot.turn(25, 2*r)
    bot.straight_position(bottom[0], bottom[1], 1)

def I_love():
    bot.set_origin(0,0,0)
    draw(True)
    bot.straight_g(40)
    bot.straight_g(-20)
    bot.turn(90, 0)
    bot.straight_g(70)
    bot.turn(0,0)
    bot.straight_g(-20)
    bot.straight_g(40)
    draw(False)
    bot.straight_position(100, 70, 1)
    draw(True)
    bot.straight_position(140, 20, 1)
    bot.turn(90, 0)
    bot.turn(-90, 20,gyro_reset=True)
    bot.turn(90, 0)
    bot.turn(-180, 20, gyro_reset=True)
    bot.get_orientation()
    print("!1",bot.x, bot.y, bot.orientation, bot.Lw.angle(), bot.Rw.angle())
    bot.straight_position(100, 70, -1)
    draw(False)

def control():
    remote = XboxController()
    while True:
        pressed = remote.buttons.pressed()
        if Button.RB in pressed:
            draw(True)
        if Button.LB in pressed:
            draw(False)
        if Button.A in pressed:
            hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)
        Ldir = remote.joystick_left()
        Rdir = remote.joystick_right()
        Lw.run((Ldir[1]+Ldir[0])*10 + Rdir[1]+Rdir[0])
        Rw.run((Ldir[1]-Ldir[0])*10 + Rdir[1]-Rdir[0])


page = 1
N_pages = 4
wait_time = 1000
skip = False
wait(wait_time)
while True:
    bot.pressme(False)
    while True:
        pressed = bot.hub.buttons.pressed()
        selected = False
        bot.pressme(True)

        #presser
        if Button.RIGHT in pressed:
            page -= 1
            hub.speaker.play_notes(["A3/50"])
            wait(150)
        if Button.LEFT in pressed:
            page += 1
            hub.speaker.play_notes(["A3/50"])
            wait(150)
        if Button.CENTER in pressed:
            hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
            selected = True
        
        #limiter
        if page > N_pages:
            page = 1
        if page < 0:
            page = N_pages
        if selected == True:
            bot.pressme(False)

        if page == 1:
            hub.display.icon(Icon.HAPPY)
            if selected == True:
                wait(wait_time)
                emogi()
                bot.hub.speaker.play_notes(["A3/50"])
                skip = True

        if page == 2:
            hub.display.icon(Flower)
            if selected == True:
                wait(wait_time)
                flower(70)
                bot.hub.speaker.play_notes(["A3/50"])
                skip = True

        if page == 3:
            hub.display.icon(Fflower)
            if selected == True:
                wait(wait_time)
                fflower(70)
                bot.hub.speaker.play_notes(["A3/50"])
                skip = True
        
        if page == 4:
            hub.display.icon(Icon.TRIANGLE_UP)
            if selected == True:
                wait(wait_time)
                control()
                bot.hub.speaker.play_notes(["A3/50"])
                skip = True

        while pressed == hub.buttons.pressed():
            wait(10)
            if skip == True:
                break
            if Button.BLUETOOTH not in hub.buttons.pressed():
                break
