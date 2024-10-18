
from tools import*
from pybricks.pupdevices import Remote
from pybricks.parameters import Button
from pybricks.tools import wait
#this file is designed for remote control testing

# Connect to the remote.
my_remote = Remote("Controler")
my_remote.light.on(Color.RED)
L_motor = PFMotor(Fco, 1, Color.BLUE, positive_direction=Direction.COUNTERCLOCKWISE)
R_motor = PFMotor(Fco, 1, Color.RED)
print("detected")
#calibrate_arm(-500)
L_speed = 0
R_speed = 0
speed_step = 1000

while True:
    # Check which buttons are pressed.
    pressed = my_remote.buttons.pressed()
    
    if Button.LEFT_PLUS in pressed:
        L_speed = speed_step
    elif Button.LEFT_MINUS in pressed:
        L_speed = -speed_step
    else:
        L_speed = 0
    if Button.RIGHT_PLUS in pressed:
        R_speed = speed_step
    elif Button.RIGHT_MINUS in pressed:
        R_speed = -speed_step
    else:
        R_speed = 0
    if Button.CENTER in pressed:
        arm.run_target(1000, 0, wait=False)
    
    Lw.run(L_speed)
    Rw.run(R_speed)
    
