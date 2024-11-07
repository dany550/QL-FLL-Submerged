from tools_II import*
print("ok ok ok ok")

# Set up all devices.
hub = PrimeHub()
left = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B)
bot = Robot(hub, 27.9, 158, left, right)
bot.set_origin(0,0,0)


async def gandalf():
    while True:
        await hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)


        

# Drive forward, turn move gripper at the same time, and drive backward.
async def main():
    await bot.straight_position(100,100,1)
    await multitask(gandalf())


# Runs the main program from start to finish.
run_task(main())