from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task
print("ok ok ok ok")

# Set up all devices.
hub = PrimeHub()
left = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B)
gripper = Motor(Port.D)
drive_base = DriveBase(left, right, 56, 114)


# Move the gripper up and down.
async def gandalf():
    while True:
        await hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)

async def shake():
    while True:
        await gripper.run_angle(500, -90)
        await gripper.run_angle(500, 90)

# Drive forward, turn move gripper at the same time, and drive backward.
async def main():
    await multitask(shake(), gandalf())


# Runs the main program from start to finish.
run_task(main())