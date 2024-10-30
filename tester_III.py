# 3rd - last step in program piramid
from tools_II import *

print("ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok")
#this file is designt for testing

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
bot = Robot(hub, 27.9, 158, Lw, Rw,)
bot.set_origin(0,0,0)
print(bot.x, bot.y, bot.avr_motor_angle, bot.Lw.angle(), bot.Rw.angle())

async def gandalf():
    while True:
        await hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)

async def shake():
    bot.straight_position(100, 100, 1)

# Drive forward, turn move gripper at the same time, and drive backward.
async def main():
    await multitask(shake(), gandalf())