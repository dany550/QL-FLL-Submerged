from F01_Tools import*
print("ok ok ok ok")

# Set up all devices.
hub = PrimeHub()
left = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B)
bot = Robot(hub, 27.9, 158, left, right)
bot.set_origin(0,0,0)


def gandalf():
    hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)

def move():
    bot.straight_position(100, 100, 1)
 
def repeat(task):
    while True:
        task()
# Drive forward, turn move gripper at the same time, and drive backward.
def main():
    print("blbalalbla")
    multitask(move(), gandalf())

def task():
    None
repeat()
# Runs the main program from start to finish.
