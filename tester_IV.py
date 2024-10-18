# 3rd - last step in program piramid
from tools import *
hub.display.orientation(Side.RIGHT)
hub.display.icon(T)
hub.system.set_stop_button((Button.BLUETOOTH))
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

def hledej(position, N):
    x = N%3 * 18.5 + 28
    y = N//3 * 18.5 + 12
    position = straight_position([x, y], 1, position)
    arma.run_target(1000, -45)
    position = turn(90, 0, origin=position)
    position = straight_g(12, position)
    return position

def skoruj(position):
    # while True:
    #     color = Cc.color()
    #     if color != Color.NONE:
    #         break
    print(color)
    if color == Color.GRAY or color == Color.GREEN or color == Color.BLUE:
        arma.run(1000)
        position = straight_g(-10, position)
        position = turn(-90, 0, origin=position)
        position = straight_position([10, 10], 1, origin=position)
        arma.run_target(1000, -45)
        
        ###
    elif color == Color.YELLOW:
        arma.run(1000)
        position = straight_g(-10, position)
        position = turn(-90, 0, origin=position)
        position = straight_position([70, 10], 1, origin=position)
        position = straight_position([80, 90], 1, origin=position)
        arma.run_target(1000, -45)
        position = straight_g(10, position)
        position = straight_position([70, 10], -1, origin=position)
        ###
    else:
        position = straight_g(-10, position)

    position = straight_position([10, 10], -1, origin=position)
    return position
        
align_wall(-500, 500)
#gyro_calib()
position = set_origin()
pressme(True)
row = 1
while True:
    pressed = hub.buttons.pressed()
    wait(10)
    if Button.CENTER in pressed:
        hub.speaker.play_notes(["A3/16", "C4/16", "E4/16"])
        break
pressme(False)
for i in range(9):
    position = hledej(position, i)
    position = skoruj(position)
    






    