from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

wheel_radius = 27 #in mm
axle_track = 158 #in mm
#wheel_circumference = 2 * pi * wheel_radius

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
robot = DriveBase(Lw, Rw, wheel_radius*2, axle_track)
robot.use_gyro(True)
robot.straight(2000)

