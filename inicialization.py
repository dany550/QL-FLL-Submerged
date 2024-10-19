from pybricks.hubs import*
from pybricks.robotics import*
from pybricks.iodevices import*
from pybricks.tools import*
from pybricks.parameters import*
from pybricks.pupdevices import*
from pybricks import*

from icons import*
from umath import*

hub = PrimeHub()
Robot = DriveBase()
Rw = Motor(Port.A)
Lw = Motor(Port.B)

arma = Motor(Port.C)
arm = arma
UltraM = Rw

default_speed = 100

Cc = ColorSensor(Port.C)

wheel_circumference = 123456
wheelRadius = 8.5
axle = 15