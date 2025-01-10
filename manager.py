from tools import *
#hub.display.orientation(Side.LEFT)
hub.system.set_stop_button((Button.BLUETOOTH))
hub.speaker.volume(100)
hub.display.icon(road)
pressme(True)
itsline = None
while True:
    pressed = hub.buttons.pressed()
    wait(10)
    if Button.CENTER in pressed and itsline != None:
        hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
        break
    if Button.LEFT in pressed:
        hub.speaker.play_notes(["A3/50"])
        hub.display.icon(line)
        itsline = True
    if Button.RIGHT in pressed:
        hub.speaker.play_notes(["A3/50"])
        hub.display.icon(sprint)
        itsline = False    

pressme(False)

if itsline:
    hub.display.icon(LINE)
    while True:
        pressed = hub.buttons.pressed()
        wait(10)
        if Button.CENTER in pressed:
            hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
            break
    ### line

else:
    hub.display.icon(SPRINT)
    while True:
        pressed = hub.buttons.pressed()
        wait(10)
        if Button.CENTER in pressed:
            hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
            break
    ### sprint