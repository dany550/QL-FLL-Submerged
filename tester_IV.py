# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing
hub = PrimeHub()
Cs = ColorSensor(Port.A)
Ul = UltrasonicSensor(Port.E)
ppresed = []
while True:
    pressed = hub.buttons.pressed()
    if pressed and not ppressed:
        print(Ul.distance())
    ppressed = list(pressed)
    wait(10)
    puncher = Arm(Port.A)
    puncher.