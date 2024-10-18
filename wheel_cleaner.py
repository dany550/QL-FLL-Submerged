from inicialization import*

def wheel_cleaner(time=24000):
    """
    This program cleans the wheels

    Parameters:
        time: Number 
    """
    # time = time / 24
    # hub.display.text("Cleaning")
    # Robot.drive(500)
    # for i in range(24):
    #     x = i % 5
    #     y = i // 5
    #     hub.display.pixel(x, y)
    #     hub.speaker.play_notes(["C4/4"])
    #     wait(time)
    # hub.display.off()
    # hub.display.text("done")
    # Robot.stop()

    Robot.drive(100000, 0)
    wait(time)

if __name__ == "__main__":
    hub.display.orientation(Side.BOTTOM)
    hub.system.set_stop_button((Button.RIGHT, Button.LEFT))
    wheel_cleaner()