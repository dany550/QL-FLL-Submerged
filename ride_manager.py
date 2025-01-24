#4th - last step in program piramid
# tohle je náš operační systém pro spouštění jízd

from tools import*
from ride1 import*
from ride2 import*
from ride3 import*
from wheel_cleaner import*

hub.display.orientation(Side.BOTTOM)
hub.display.icon(lime)
hub.system.set_stop_button((Button.RIGHT, Button.LEFT))
page = 1
wait_time = 1000
skip = False

# Wheel cleaner starter
# Nové (mohlo by dělat bordel)
# LEFT = na kostce pravé (protože je vzhůru nohama)
if (Button.LEFT) in hub.buttons.pressed() and Button.BLUETOOTH not in hub.buttons.pressed():
    wheel_cleaner()
if (Button.RIGHT) in hub.buttons.pressed() and Button.BLUETOOTH not in hub.buttons.pressed():
    while True:
        hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)
while True:
    pressme(False)
    arm_shaker()
    while True:
        pressed = hub.buttons.pressed()
        selected = False
        pressme(True)

        #presser
        if Button.RIGHT in pressed:
            page -= 1
            if page <= 0:
                page = 3
            for _ in range(page):
                hub.speaker.play_notes(["A3/50"])
                wait(150)
        if Button.LEFT in pressed:
            page += 1
            if page >= 4:
                page = 1
            for _ in range(page):
                hub.speaker.play_notes(["A3/50"])
                wait(150)
        if Button.CENTER in pressed:
            hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
            selected = True


        if Button.BLUETOOTH not in pressed:
            hub.display.icon(lime)
            if skip == True:
                page += 1
            wait(1000)
            break
        
        #limiter
        if page >= 4:
            page = 1
        if page <= 0:
            page = 3

        #starter
        if selected == True:
            pressme(False)

        if page == 1:
            hub.display.icon(one)
            if selected == True:
                hub.display.icon(ONE)
                wait(wait_time)
                ride1()
                skip = True

        if page == 2:
            hub.display.icon(two)
            if selected == True:
                hub.display.icon(TWO)
                wait(wait_time)
                ride2()
                skip = True

        if page == 3:
            hub.display.icon(three)
            if selected == True:
                hub.display.icon(THREE)
                wait(wait_time)
                ride3()
                skip = True

        while pressed == hub.buttons.pressed():
            wait(10)
            if skip == True:
                break
            if Button.BLUETOOTH not in hub.buttons.pressed():
                break
