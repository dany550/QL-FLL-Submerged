from pybricks.iodevices import XboxController
from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.robotics import Car

hub = TechnicHub()
engine = Motor(Port.D)
wheel = Motor(Port.B)
car = Car(wheel, engine)

def control():
    remote = XboxController()
    while True:
        pressed = remote.buttons.pressed()
        Ldir = remote.joystick_left()
        triggers = remote.triggers()
        car.drive_power(Ldir[1] + triggers[0] - triggers[1])
        car.steer(Ldir[0])
        if Button.B in pressed:
            hub.light.on(Color.RED)

control()