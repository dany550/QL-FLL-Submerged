# 3rd - last step in program piramid
from tools import *
hub.display.orientation(Side.RIGHT)
hub.display.icon(T)
hub.system.set_stop_button((Button.BLUETOOTH))
print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

origin = set_origin()
origin = straight_position([30,0],1, origin)
print(origin)