from inicialization import*

def arm_setup_data(arm, speed, stress=1):
    """
    stops the motor as soon as it meets resistance

    Parameters:
        - arm: {La, Ra, Lw, Rw}
        - speed: Number - deg/s (+ clockwise, - counterclockwise)
        - stress: Number - if the motor is under upnormal stress, change stress <0.25; 8>. More stress means harder resistence of motor.
    """
    #working

    speed = clamp(abs(speed), 1000, 100)*abs(speed)/speed
    stress = clamp(abs(stress), 8, 0.25)
    cons = abs(clamp(800/abs(speed), 6, 1.5))*stress
    #cons(constant) = how many times the motor speed has to decrease to stop the motor.
    #time is time until the motor speeds up
    return [arm, speed, cons]

def arm_strter(data, waiting):
    arm = data[0]
    speed = data[1]

    arm.run(speed)

def arm_braker(data):
    """
    loop part
    """
    arm = data[0]
    speed = data[1]
    cons = data[2]

    arm_speed = abs(arm.speed())
    #print(arm_speed, "/", speed)
    if arm_speed < abs(speed/cons):
        arm.stop()
        break

def robot_setup2(La_align_use, La_speed, Ra_align_use, Ra_speed, align_wall_speed, calib_gyro, gyro_angle, La_stress=1, Ra_stress=1):
    """
    Parameters:
        - La_aling_use: Logic - wants to know if left amr might be alinged.
        - La_speed: Number - deg/s - speed to aling arm (+ clockwise, - counterclockwise)
        - La_stress: Number - stress of left arm. if the motor is under upnormal stress, change stress <0.25; 8>. More stress means harder resistence of motor.
        
        - Ra_aling_use: Logic - wants to know if right amr might be alinged.
        - Ra_speed: Number - deg/s - speed to aling arm (+ clockwise, - counterclockwise)
        - Ra_stress: Number - stress of right arm. if the motor is under upnormal stress, change stress <0.25; 8>. More stress means harder resistence of motor.

        - aling_wall_speed: Number - deg/s
        - gyro_calib: Logic
    """
    #working

    
    #arm aligner
    La_data = arm_setup_data(La, La_speed, stress=La_stress)
    Ra_data = arm_setup_data(Ra, Ra_speed, stress=Ra_stress)


    if La_align_use == True:
       
    if Ra_align_use == True:
        
    align_wall(align_wall_speed, 2000)
    if calib_gyro == True:    
        wait(500)
        gyro_calib(angle=gyro_angle)

    pressme(True)
    while not any([x for x in hub.buttons.pressed() if x not in [Button.BLUETOOTH]]):
        wait(10)
    pressme(False)
    return None






