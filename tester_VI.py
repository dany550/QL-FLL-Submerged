from tools import*
from pybricks.robotics import DriveBase
wheel_radius = 27.9 #in mm
axle_track = 158 #in mm
#wheel_circumference = 2 * pi * wheel_radius



hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
robot = DriveBase(Lw, Rw, wheel_radius*2, axle_track)
robot.settings(straight_speed=900)
bot = Robot(hub, wheel_radius, axle_track, Lw, Rw)
#robot.use_gyro(True)
#robot.straight(2000)
#wait(2000)
bot.set_origin(0,0,0)
#bot.turn(-90, 50)
bot.straight_position(-100,100,-1)
#bot.straight_g(2000)
#wait(2000)
#robot.straight(-2000)
bot.straight_position(0,0,1)
#bot.straight_g(-2000)