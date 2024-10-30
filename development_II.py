from tools import*

def set_origin():
    origin = [0, 0, 0]
    return origin

def update_origin(origin):
    
    distance = (La.angle() + Ra.angle())/2
    alfa = hub.imu.heading()
    x = cos(alfa) * distance
    y = sin(alfa) * cistance
    origin[0] = alfa
    origin[1] = origin[1] + x
    origin[2] = origin[2] + y
    return origin

def back_to_origin(origin):
    alfa = origin[0]
    x = origin[1]
    y = origin[2]
    tan_alfa = x/y
    angle = atan(tan_alfa) + 180
    distance = sqrt(x*x+y*y) * (-1)
    
    turn_2_g(angle, gyro_reset=False)
    straight_g(distance)
    turn_2_g(180)

def straight_g_u(til_distance, speed=default_speed, set_angle = False, angle = 0):
    """
    extra precise straight movement
     
    Parameters:
        - length: Number - cm
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    # lenght to mm
    length = length*10
    time = 10
    cons = 25
    #gyroconstant

    Lw.reset_angle(0)
    Rw.reset_angle(0)
    L_wheel = True
    R_wheel = True
    #wait(200)
    start_angle = hub.imu.heading()

    while True:       
        L_angle = Lw.angle()
        R_angle = Rw.angle()
        L_motor_speed = Lw.speed(time)
        R_motor_speed = Rw.speed(time)
        U_distance = FUl.distance()

        if set_angle == True:
            angle = hub.imu.heading() - angle
        else:
            angle = hub.imu.heading() - start_angle

        new_speed = accelerator(til_distance, (L_motor_speed + R_motor_speed)/2 , U_distance, speed)

        L_speed = new_speed

        #motor corector
        R_speed = angle * cons + new_speed

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        #motor breaker
        if til_distance > U_distance:
            Lw.stop()
            L_wheel = False
            Rw.stop()
            R_wheel = False
            break
        wait(10)
        #print(L_angle, R_angle, "/", motor_angle)

def turn_2_gutest(angle, speed=default_speed/4, gyro_reset=True):
    """
    - Especially accurate turning by 2 wheels.
    - Based on Gyro checked by motor angle

    Parameters:
        - angle: Number - deg - (positive forward, negative backward)
        - speed: Number - deg/s 
    """
    if gyro_reset == True:
        start_angle = hub.imu.heading()
        motor_start_angle = 0
    else:
        start_angle = 0
        motor_start_angle = hub.imu.heading()
    
    cons = clamp(4000/speed,20,5)
    trajectory = axle_track*pi
    motor_angle = (trajectory/wheel_circumference) * (angle - motor_start_angle)
    gyro_error = False

    Lw.reset_angle(0)
    Rw.reset_angle(0)

    while True:
        actual_angle = hub.imu.heading() - start_angle
        L_motor_angle = Lw.angle()
        R_motor_angle = Rw.angle()
        print(FUl.distance(), actual_angle)

        if gyro_error == False:
            motor_speed = absclamp((angle - actual_angle)*cons, speed, 2)
            Lw.run(motor_speed)
            Rw.run(-motor_speed)
            if abs(abs(angle)-abs(actual_angle))<=0.4:
                #print(actual_angle, "/",angle)
                Lw.brake()
                Rw.brake()
                break
            if abs(L_motor_angle) > abs(motor_angle) + 180:
                #print(L_motor_angle, "/", motor_angle)
                for i in range(4):
                    hub.speaker.beep(500, 50)
                    wait(50)
                gyro_error = True

        else:
            L_motor_speed = absclamp((motor_angle - L_motor_angle) * cons, speed, 5)
            
            #motor controler
            R_motor_speed = motor_corector(L_motor_angle, R_motor_angle, L_motor_speed)
        
            Lw.run(L_motor_speed)
            Rw.run(-R_motor_speed)

            #break
            if (abs(L_motor_angle) + abs(R_motor_angle)) / 2 > motor_angle:
                Lw.stop()
                Rw.stop()
                break

def straight_gu(til_distance, speed=default_speed, origin = 0, set_angle = False, angle = 0):
    """
    extra precise straight movement
     
    Parameters:
        - length: Number - cm
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    # lenght to mm
    til_distance = til_distance*10
    time = 10
    cons = 15
    #gyroconstant

    Lw.reset_angle(0)
    Rw.reset_angle(0)
    L_wheel = True
    R_wheel = True
    #wait(200)
    start_angle = hub.imu.heading()

    while True:       
        L_angle = Lw.angle()
        R_angle = Rw.angle()
        L_motor_speed = Lw.speed(time)
        R_motor_speed = Rw.speed(time)
        Ul_distance = FUl.distance()

        if set_angle == True:
            angle = hub.imu.heading() - angle
        else:
            angle = hub.imu.heading() - start_angle

        new_speed = accelerator(til_distance, (L_motor_speed + R_motor_speed) / 2, Ul_distance, speed, brake_radius=200)

        L_speed = new_speed

        #motor corector
        R_speed = angle * cons + new_speed

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        #motor breaker
        if til_distance > Ul_distance:
            Lw.stop()
            L_wheel = False
            Rw.stop()
            R_wheel = False
            break
        if origin != 0:
           origin = update_origin(origin) 
        wait(10)

    if origin != 0:
        wait(100)
        origin = update_origin(origin) 
        return origin

def skenerror(value, max_distance, speed, origin = 0, set_angle = False, angle = 0):
    """
    extra precise straight movement
     
    Parameters:
        - length: Number - cm
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    # lenght to mm
    value = value * 10
    max_distance = max_distance * 10
    time = 10
    cons = 15
    #gyroconstant

    Lw.reset_angle(0)
    Rw.reset_angle(0)
    L_wheel = True
    R_wheel = True
    #wait(200)
    start_angle = hub.imu.heading()
    max_motor_angle = (max_distance/wheel_circumference*360)

    while True:       
        L_angle = Lw.angle()
        R_angle = Rw.angle()
        L_motor_speed = Lw.speed(time)
        R_motor_speed = Rw.speed(time)
        Ul_distance = LUl.distance()

        if set_angle == True:
            angle = hub.imu.heading() - angle
        else:
            angle = hub.imu.heading() - start_angle

        new_speed = accelerator((L_angle + R_angle) / 2, (L_motor_speed + R_motor_speed) / 2, max_motor_angle, speed)
        L_speed = new_speed

        #motor corector
        R_speed = angle * cons + new_speed

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        #motor breaker
        if  Ul_distance > value or (L_angle+R_angle)/2 > max_motor_angle:
            Lw.stop()
            L_wheel = False
            Rw.stop()
            R_wheel = False
            break
        if origin != 0:
           origin = update_origin(origin) 
        wait(10)

    if origin != 0:
        wait(100)
        origin = update_origin(origin) 
        return origin

