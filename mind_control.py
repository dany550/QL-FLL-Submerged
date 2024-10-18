from inicialization import*


L_motor = PFMotor(Fco, 1, Color.BLUE, positive_direction=Direction.COUNTERCLOCKWISE)
R_motor = PFMotor(Fco, 1, Color.RED)
print("detected")

while True:
    L_motor.()
    R_motor.stop()