from tools import*
from pybricks.robotics import DriveBase
wheel_radius = 27.9 #in mm
axle_track = 158 #in mm
#wheel_circumference = 2 * pi * wheel_radius



hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, wheel_radius, axle_track, Lw, Rw)
print(hub.system.storage(40,))