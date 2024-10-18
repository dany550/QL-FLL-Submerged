#2nd step of program piramid
from inicialization import*

#Mathematical functions
def clamp(value: Number, maxi: Number, mini: Number):
    """
    keeps the value between maximum and minimum

    Parameters:
        - value: Number
        - maxi: Number
        - mini: Number

    Returns:
        - value between maximum and minimum
    """
    if maxi >= value >= mini:
        final_value = value
    elif maxi < value:
        final_value = maxi
    elif mini > value:
        final_value = mini
    return(final_value)

def absclamp(value: Number, maxi: Number, mini: Number):
    """
    keeps absolute value of the value between maximum and minimum

    Parameters:
        - value: Number
        - maxi: Number
        - mini: Number

    Returns:
        - value number
    """
    maxi = abs(maxi)
    mini = abs(mini)
    if maxi >= abs(value) >= mini:
        final_value = value
    elif value == 0:
        final_value = 0
    elif maxi < abs(value):
        final_value = maxi*value/abs(value)
    elif mini > abs(value):
        final_value = mini*value/abs(value)
    return(final_value)

def motor_corector(L_angle, R_angle, speed, ratio: Number=1, extra_condition=True):
    """
    - this function calculates speed of one motor (right) from difference of motor angles
    - this could be use only for functions which use both wheels
    - 'vyrovnávač pohybu'

    Parameters:
        - L_angle: Number - deg - motor angle of the motor whose speed isn't calculated by this function (left)
        - R_angle: Number - deg - motor angle of the motor whose speed is calulated by this function (right)
        - speed: Number - deg/s
        - extra_condition: if you have some conditions when to calculate and when not, write them here
    """
    constant = 1
    # this constant is how strong the motor corection might be
    if extra_condition:
        R_speed = absclamp(((L_angle-R_angle)*constant)+speed, 2*speed, speed/2)*ratio
        #print(((L_angle-R_angle)*constant)+speed)
    else:
        R_speed = speed
    return R_speed

def accelerator(
    actual_motor_angle: Number, 
    motor_angle: Number, 
    speed: Number, 
    acceleration: Number = 1,
    deceleration: Number = 1,
    min_speed: Number = 50,
    start_speed: Number = 50,
    terminal_speed: Number = 50
    ):
    """
    - This function works with the robot's speed and modifies it for a smooth start and stop.
    - This function is designed for being part of a loop.
    - It's recomentded to place this before motor corector.
    - This function could cause slower reactions of robot.

    Parameters:
        - actual_motor_angle: Number - deg - mesured motor angle, if you work with 2 motor movement, place here average angle of both motors.
        - motor_angle: Number - deg - AIM angle
        - speed: Number - deg/s - raw speed

    uses: calmp, absclamp
    """
    
    acceleration = abs(acceleration)
    deceleration = abs(deceleration)

    if deceleration == 0 or motor_angle == 0:
        max_speed = speed
    else:
        max_speed = absclamp((motor_angle - actual_motor_angle)/(deceleration*0.36), speed, terminal_speed)

    if acceleration == 0:
        new_speed = max_speed
    else:
        new_speed = absclamp((actual_motor_angle/(acceleration*3.6))**2 + abs(start_speed) + min_speed, max_speed, min_speed)

    new_speed = new_speed * motor_angle / abs(motor_angle)

    return new_speed

#code parts
def pressme(on: bool, color = Color.CYAN):
    """
    highlights central button

    Parameters:
        on: Logic (True - highlight, False - turn light off)
    """
    if on == True:
        hub.light.blink(color, [500, 50, 200, 50])
    else:
        hub.light.on(color)

def motor_driver(L_speed: Number, R_speed: Number, L_wheel: bool, R_wheel: bool):
    """
    - this function turns of motor based on logic imput

    Parameters
        - L_speed: Number - deg/s
        - R_speed: Number - deg/s
        - L_wheel: Logic
        - R_wheel: Logic
    """
    if L_wheel == True:
        Lw.run(L_speed)
    else:
        Lw.brake()
    if R_wheel == True:
        Rw.run(R_speed)
    else:
        Rw.brake()

def update_origin(origin: list, avr_motor_angle: Number, angle: Number):
    """
    Parameters
        - origin: list
        - avr_motor_angle: Number
        - angle: Number
    """
    
    if abs(origin[2]) - 10 > abs(avr_motor_angle):
        motor_dif = avr_motor_angle
    else:
        motor_dif = avr_motor_angle - origin[2]

    distance = (motor_dif/360)*wheel_circumference/10
    #print(La.angle(), Ra.angle(), distance)
    #print(sin(alfa), cos(alfa))
    x = cos(radians(angle)) * distance
    y = sin(radians(angle)) * distance
    origin[0] = origin[0] + x
    origin[1] = origin[1] + y
    origin[2] = avr_motor_angle
    #print(origin, x, y)
    return origin

def Ultra_read(angle: Number):
    """
    Parameters
        - angle: Number
    """

    angle = clamp(angle, 180, -180)
    if angle != UltraM.angle():
        UltraM.run_target(1000, angle)
    
    Ultra_angle = UltraM.angle()
    distance = Bul.distance()
    return(distance)

def bear_detector(normal_distance: Number = 300):
    """
    Parameters
        - normal_distance: Number
    """

    if Ful.distance() > normal_distance:
        arm.run(1000)
        detected = True
    else:
        detected = False
    return detected

#calibration functions
def set_origin(x: Number = 0, y: Number = 0):
    origin = [0, 0, 0, False, False]
    return origin

def gyro_calib(angle: Number=0, vypnout: bool=True):
    """
    could be extremly extremly extremly slow
    """
    accuracy_1 = 0.0007
    accuracy_2 = 0.001


    if vypnout:
        accuracy_2 = 0.05

    while True:

        hub.imu.reset_heading(angle)
        wait(100)
        if abs(hub.imu.heading()-angle) <= accuracy_1:    # bylo 0.0005
            wait(100)
            if abs(hub.imu.heading()-angle) <= accuracy_2:
                hub.speaker.play_notes(["C4/10", "F4/10"])
                print("calibrated")
                gyro_error = False
                break
        print(hub.imu.heading())
            #hub.speaker.beep(500,10)

def Ultra_setup(angle: Number, wait: bool = False):
    angle = clamp(angle, 180, -180)
    UltraM.run_target(1000, angle, wait=wait)

def def_radar_data():
    data = {}
    radar_data = [0, data]
    return radar_data

#sensor control
def radar_sken(radar_data: list, speed: Number = 1000, max_angle: Number = 170, min_angle: Number = -170, refresh: bool = True):
    """
    Parameters
        - radar_data = [0, []]
    """
    N = radar_data[0]
    total_angle = (max_angle - min_angle)
    parity = (N // total_angle) % 2
    angle_shift = N % total_angle 

    if parity == 0:
        angle = min_angle + angle_shift
    else:
        angle = max_angle - angle_shift

    data = radar_data[1]
    for i in range(10):
        try:
           del data[angle+i] 
        except KeyError:
            none=1
    
    UltraM.run_target(speed, angle, wait=False)
        
        #print("del")

    m_angle = UltraM.angle()
    distance = Bul.distance()
    data[m_angle] = distance

    if abs(angle - m_angle) <= 20:
        N += 8
    radar_data = [N, data]
    return radar_data 

#Motion functions
def straight_g(length: Number, origin: list, speed: Number=default_speed, terminal_speed: Number = 50, set_angle: bool = False, angle: Number = 0, bear = False):
    """
    extra precise straight movement
     
    Parameters:
        - length: Number - in cm
        - speed: Number - in deg/s
        - origin: list
        - terminal_speed: Number - in deg/s
        - set_angle: bool
        - angle: Number - in deg
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    if origin[3] and bear:
        return origin

    # lenght to mm
    length = length*10
    time = 10
    g_cons = 20
    corector_cons = 10
    #gyroconstant

    L_start_angle = Lw.angle()
    R_start_angle = Rw.angle()
    L_wheel = True
    R_wheel = True
    motor_angle = (length/wheel_circumference*360)
    L_speed = Lw.speed(window=10)
    R_speed = Rw.speed(window=10)
    avr_start_speed = (L_speed + R_speed)/2

    if set_angle == False:
        start_angle = hub.imu.heading()
    else:
        start_angle = angle

    terminal_speed = clamp(terminal_speed, 900, 50)
    if terminal_speed == 50:
        stop = True
    else:
        stop = False

    start = [0, 0, 0]

    x = cos(radians(start_angle)) * length/10
    y = sin(radians(start_angle)) * length/10
    finish = [x + start[0], y + start[1], 0]
    
    while True:       
        L_angle = Lw.angle() - L_start_angle
        R_angle = Rw.angle() - R_start_angle
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading() - start_angle
        start = update_origin(start, avr_motor_angle, angle)

        #print(L_angle, R_angle)
        new_speed = accelerator(start[2], motor_angle, speed, start_speed=avr_start_speed, terminal_speed=terminal_speed)

        #print(new_speed, ";", start[0], ";", finish[0])
        L_speed = new_speed - angle * g_cons - start[1] * corector_cons

        #motor corector
        R_speed = new_speed + angle * g_cons + start[1] * corector_cons

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        if bear:
            caught = bear_detector()
        else:
            caught = False

        #motor breaker
        if abs(R_angle) + abs(L_angle) > abs(motor_angle)*2 or caught:
            #print("vypínač")
            if stop == True:
                Lw.stop()
                Rw.stop()
                L_wheel = False
                R_wheel = False
            break
 
        wait(10)

    origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], caught, origin[4]]
    #origin = [cos(radians(start_angle))*length/10 + origin[0], sin(radians(start_angle))*length/10 + origin[1], origin[2] + start[2]]
    return origin

        #print(L_angle, R_angle, "/", motor_angle)

def straight_position(finish: list, direction: Number, origin: list, speed: Number=default_speed, terminal_speed: Number = 50):
    """
    extra precise straight movement
     
    Parameters:
        - finish: list [x, y] - in cm
        - origin: list [x, y] - in cm - use origin system
        - speed: Number - in deg/s
        - terminal_speed: Number - in deg/s
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """

    #constants
    time = 10
    g_cons = 20
    corector_cons = 10 * direction

    #trajectory calculator
    direction = absclamp(direction, 1, 1)
    x_shift = (finish[0] - origin[0])*direction
    y_shift = (finish[1] - origin[1])*direction
    length = sqrt(x_shift**2 + y_shift**2)*10*direction
    if length == 0:
        return origin   
    start_angle = degrees(atan2(y_shift, x_shift))
    if start_angle - hub.imu.heading() > 180:
        start_angle -= 360
    elif start_angle - hub.imu.heading() < -180:
        start_angle += 360

    #print(length, start_angle)

    #setup
    L_start_angle = Lw.angle()
    R_start_angle = Rw.angle()
    L_wheel = True
    R_wheel = True
    motor_angle = (length/wheel_circumference*360)
    L_speed = Lw.speed(window=10)
    R_speed = Rw.speed(window=10)
    avr_start_speed = (L_speed + R_speed)/2

    terminal_speed = clamp(terminal_speed, 900, 50)
    if terminal_speed == 50:
        stop = True
    else:
        stop = False

    start = [0, 0, 0]
    
    while True:       
        L_angle = Lw.angle() - L_start_angle
        R_angle = Rw.angle() - R_start_angle
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading() - start_angle
        start = update_origin(start, avr_motor_angle, angle)

        #print(start_angle,angle)
        new_speed = accelerator(start[0]/wheel_circumference*3600, motor_angle, speed, start_speed=avr_start_speed, terminal_speed=terminal_speed)

        #print(new_speed, ";", start[0], ";", length)
        L_speed = new_speed - angle * g_cons - start[1] * corector_cons

        #motor corector
        R_speed = new_speed + angle * g_cons + start[1] * corector_cons

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        #motor breaker
        if abs(start[0]) > abs(length/10):
            if stop == True:
                Lw.stop()
                Rw.stop()
                L_wheel = False
                R_wheel = False
            break
 
        wait(10)

    origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], origin[3], origin[4]]
    return origin

        #print(L_angle, R_angle, "/", motor_angle)

def turn(angle: Number, radius: Number, speed: Number=default_speed, origin: list = [], stop: bool=True, gyro_use: bool=True, gyro_reset: bool=False, bear = False):
    """
    Parameters:
        - angle: Number - in deg - positive = forward, if multiple of angle and radius positive = clockwise
        - radius: Number - in mm - positive = Lw faster, if multiple of angle and radius positive = clockwise, special cases: 0 -> turn_2, axle_track/2 -> turn_1
        - speed: Number - in deg/s - it's recommended to slow down if the radius is too small
        - origin: list - coordinate global positioning system (c GPS)
        - stop: bool - than stop or not?
        - gyro_use: bool - do you want to use gyro? (yes you want, everybody wants)
        - gyro_reset: bool - reset gyro or not?
    """
    #angle corector
    if bear and origin[3]:
        return origin

    if gyro_reset == True:
        start_angle = hub.imu.heading()
        motor_start_angle = 0
    else:
        start_angle = 0
        motor_start_angle = hub.imu.heading()
    
    #speed calculator
    if radius >= 0:
        Rw_ratio = clamp((radius - axle_track/2)/abs(radius + axle_track/2), 1, -1)
    else:
        Rw_ratio = -1
    if radius <= 0:
        Lw_ratio = clamp((radius + axle_track/2)/abs(radius - axle_track/2), 1, -1)
    else:
        Lw_ratio = 1
    print(Lw_ratio, Rw_ratio)

    #setup
    cons = clamp(4000/speed + abs(radius)/10 ,50,5)
    trajectory = (abs(radius) + axle_track/2)*pi
    motor_angle = (trajectory/wheel_circumference) * (angle - motor_start_angle)
    
    if gyro_use == True:
        gyro_error = False
    else:
        gyro_error = True

    start = [0, 0, 0]

    #motor setup
    L_speed = Lw.speed(window=10)
    R_speed = Rw.speed(window=10)
    avr_start_speed = (L_speed + R_speed)/2
    L_start_angle = Lw.angle()
    R_start_angle = Rw.angle()

    #main loop
    while True:
        #reeder
        actual_angle = hub.imu.heading() - start_angle
        angle_dif = angle - actual_angle
        L_motor_angle = Lw.angle() - L_start_angle
        R_motor_angle = Rw.angle() - R_start_angle
        avr_motor_angle = (L_motor_angle + R_motor_angle)/2
        start = update_origin(start, avr_motor_angle, actual_angle)
        #print(Lw.speed(),";", Rw.speed(),";", actual_angle,";", L_motor_angle,";", R_motor_angle)
        new_speed = accelerator(abs(L_motor_angle)+abs(R_motor_angle), 1, speed, start_speed=avr_start_speed, deceleration=False)

        #core
        if gyro_error == False:

            #speed calculator
            
            if stop == True:
                motor_speed = absclamp(angle_dif*cons, new_speed, 2)
            else:
                motor_speed = speed * angle_dif/abs(angle_dif)
            #print(motor_speed)

            #motor driver
            Lw.run(motor_speed * Lw_ratio)
            Rw.run(motor_speed * Rw_ratio)

            #print(actual_angle, "/",angle)

            #motor braker
            if abs(abs(angle)-abs(actual_angle))<=1:
                
                if stop == True:
                    Lw.brake()
                    Rw.brake()
                break

            #check
            if abs(L_motor_angle + R_motor_angle)/2 > abs(motor_angle) + 3600:
                #print(L_motor_angle, "/", motor_angle)
                for i in range(4):
                    hub.speaker.beep(500, 50)
                    wait(50)
                gyro_error = True
                stop = True

        #error
        else:
            if stop == True:
                L_motor_speed = absclamp((motor_angle - L_motor_angle) * cons, new_speed, 5)
            else:
                L_motor_speed = new_speed
            
            #motor controler
            R_motor_speed = motor_corector(L_motor_angle, R_motor_angle, L_motor_speed)
        
            Lw.run(L_motor_speed * Lw_ratio)
            Rw.run(R_motor_speed * Rw_ratio)

            #break
            if (abs(L_motor_angle) + abs(R_motor_angle)) / 2 > motor_angle:
                Lw.stop()
                Rw.stop()
                break
    
    if origin:
        if stop == True:
            wait(100)
        #start = update_origin(start, (Rw.angle() + Lw.angle())/2, hub.imu.heading() - start_angle) 
        origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], origin[3], origin[4]]
        #origin = [cos(radians(start_angle))*length/10 + origin[0], sin(radians(start_angle))*length/10 + origin[1], origin[2] + start[2]]
        return origin

#Specialized functions
def skener(speed, value, max_distance, origin, set_angle = False, angle = 0, Ul_angle = 180, size = 10, bear = True):
    """
    extra precise straight movement
     
    Parameters:
        - speed: Number - deg/s
        - value: Number - mm
        - max_distance: Number - in cm
        - origin: list
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    if origin[3] and bear:
        return origin

    Ultra_setup(Ul_angle)
    # lenght to mm
    length = max_distance*10
    time = 10
    g_cons = 25
    corector_cons = 10
    #gyroconstant

    Lw.reset_angle(0)
    Rw.reset_angle(0)
    L_wheel = True
    R_wheel = True
    ul_distance = {}
    ul_data = []
    motor_angle = (length/wheel_circumference*360)
    #print(motor_angle)

    if set_angle == False:
        start_angle = hub.imu.heading()
    else:
        start_angle = angle

    start = [0, 0, 0]

    x = cos(radians(start_angle)) * length
    y = sin(radians(start_angle)) * length
    finish = [x + start[0], y + start[1], 0]
    #print(finish, y)
    
    while True:       
        L_angle = Lw.angle()
        R_angle = Rw.angle()
        #print(Ultra_read(Ul_angle))
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading() - start_angle
        start = update_origin(start, avr_motor_angle, angle)
        #ul_distance[floor(start[0]*5)] = Ultra_read(Ul_angle)
        ul_data.append(Ultra_read(Ul_angle))
        if len(ul_data) > size:
            ul_data.pop(0)

        #print(ul_distance)
        new_speed = accelerator(start[2], motor_angle, speed)

        #detection
        N = len(ul_data)-1
        if N >= size - 1:
            for i in range(size):
                detected = False
                if ul_data[N-i] > value:
                    detected = True
                else:
                    break
        else:
            detected = False

        #print(Lw.speed(),";", Rw.speed(), ";", new_speed)
        L_speed = new_speed - angle * g_cons - start[1] * corector_cons

        #motor corector
        R_speed = new_speed + angle * g_cons + start[1] * corector_cons

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        if bear:
            caught = bear_detector()
        else:
            caught = False
        
        #motor breaker
        if abs(R_angle) + abs(L_angle) > abs(motor_angle)*2 or detected or caught:
            #print("vypínač")
            Lw.stop()
            L_wheel = False
            Rw.stop()
            R_wheel = False
            #print("vypínač2")
            break
            #print("vypínač3")
        wait(10)

    #for value in ul_distance:
    #    print(value, ";", ul_distance[value])
    #print(start[0], ul_distance)
    origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], caught, detected]
    #origin = [cos(radians(start_angle))*length/10 + origin[0], sin(radians(start_angle))*length/10 + origin[1], origin[2] + start[2]]
    return origin


        #print(L_angle, R_angle, "/", motor_angle)

def straight_uhni(length: Number, origin: list, speed = 200, terminal_speed: Number = 50, set_angle: bool = False, angle: Number = 0, bear = False, pre_angle = 0):
    """
    extra precise straight movement
     
    Parameters:
        - length: Number - in cm
        - speed: Number - in deg/s
        - origin: list
        - terminal_speed: Number - in deg/s
        - set_angle: bool
        - angle: Number - in deg
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """
    if origin[3] and bear:
        return origin

    # lenght to mm
    radar_data = def_radar_data()
    length = length*10
    time = 10
    g_cons = 20
    corector_cons = 10
    critical_distance = 250
    #gyroconstant


    L_g_off = 1
    R_g_off = 1
    cor_off = 1

    L_start_angle = Lw.angle()
    R_start_angle = Rw.angle()
    L_wheel = True
    R_wheel = True
    motor_angle = (length/wheel_circumference*360)
    L_speed = Lw.speed(window=10)
    R_speed = Rw.speed(window=10)
    avr_start_speed = (L_speed + R_speed)/2

    if set_angle == False:
        start_angle = hub.imu.heading()
    else:
        start_angle = angle

    terminal_speed = clamp(terminal_speed, 900, 50)
    if terminal_speed == 50:
        stop = True
    else:
        stop = False

    start = [0, 0, 0]

    x = cos(radians(start_angle)) * length/10
    y = sin(radians(start_angle)) * length/10
    finish = [x + start[0], y + start[1], 0]
    
    while True:       
        L_angle = Lw.angle() - L_start_angle
        R_angle = Rw.angle() - R_start_angle
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading() - start_angle
        start = update_origin(start, avr_motor_angle, angle)
        radar_data = radar_sken(radar_data)

        #print(L_angle, R_angle)
        new_speed = accelerator(start[2], motor_angle, speed, start_speed=avr_start_speed, terminal_speed=terminal_speed)



        for value in radar_data[1]:
            distance = radar_data[1][value]
            if distance <= critical_distance:
                if value <= pre_angle:
                    L_uhni_cons = 0
                    R_g_off = 0.08
                    cor_off = 0.4
                    break
                else:
                    R_uhni_cons = 0
                    L_g_off = 0.08
                    cor_off = 0.4
                    break
            else:
                L_uhni_cons = 1
                R_uhni_cons = 1
        #print(L_uhni_cons, R_uhni_cons)

        #print(new_speed, ";", start[0], ";", finish[0])
        L_speed = (new_speed - (angle * g_cons)*L_g_off + start[1] * corector_cons * cor_off) * L_uhni_cons

        #motor corector
        R_speed = (new_speed + (angle * g_cons)*R_g_off - start[1] * corector_cons * cor_off) * R_uhni_cons

        #print(L_speed, R_speed)



        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        if bear:
            caught = bear_detector()
        else:
            caught = False

        #motor breaker
        if abs(R_angle) + abs(L_angle) > abs(motor_angle)*2 or caught:
            #print("vypínač")
            if stop == True:
                Lw.stop()
                Rw.stop()
                L_wheel = False
                R_wheel = False
            break
 
        wait(10)

    origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], caught, origin[4]]
    #origin = [cos(radians(start_angle))*length/10 + origin[0], sin(radians(start_angle))*length/10 + origin[1], origin[2] + start[2]]
    return origin

def straight_fake_uhni(finish: list, direction: Number, origin: list, speed: Number=default_speed, terminal_speed: Number = 50):
    """
    extra precise straight movement
     
    Parameters:
        - finish: list [x, y] - in cm
        - origin: list [x, y] - in cm - use origin system
        - speed: Number - in deg/s
        - terminal_speed: Number - in deg/s
    
    uses: accelerator, motor_controler, motor_driver, clamp, absclamp
    """

    #constants
    time = 10
    g_cons = 20
    corector_cons = 10 * direction

    #trajectory calculator
    radar_data = def_radar_data()
    direction = absclamp(direction, 1, 1)
    x_shift = (finish[0] - origin[0])*direction
    y_shift = (finish[1] - origin[1])*direction
    length = sqrt(x_shift**2 + y_shift**2)*10*direction
    if length == 0:
        return origin   
    start_angle = degrees(atan2(y_shift, x_shift))
    if start_angle - hub.imu.heading() > 180:
        start_angle -= 360
    elif start_angle - hub.imu.heading() < -180:
        start_angle += 360

    print(length, start_angle)

    #setup
    L_start_angle = Lw.angle()
    R_start_angle = Rw.angle()
    L_wheel = True
    R_wheel = True
    motor_angle = (length/wheel_circumference*360)
    L_speed = Lw.speed(window=10)
    R_speed = Rw.speed(window=10)
    avr_start_speed = (L_speed + R_speed)/2

    terminal_speed = clamp(terminal_speed, 900, 50)
    if terminal_speed == 50:
        stop = True
    else:
        stop = False

    start = [0, 0, 0]
    
    while True:       
        L_angle = Lw.angle() - L_start_angle
        R_angle = Rw.angle() - R_start_angle
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading() - start_angle
        start = update_origin(start, avr_motor_angle, angle)
        radar_data = radar_sken(radar_data)

        #print(start_angle,angle)
        new_speed = accelerator(start[0]/wheel_circumference*3600, motor_angle, speed, start_speed=avr_start_speed, terminal_speed=terminal_speed)

        #print(new_speed, ";", start[0], ";", length)
        L_speed = new_speed - angle * g_cons - start[1] * corector_cons

        #motor corector
        R_speed = new_speed + angle * g_cons + start[1] * corector_cons

        #print(L_speed, R_speed)

        motor_driver(L_speed, R_speed, L_wheel, R_wheel)

        #motor breaker
        if abs(start[0]) > abs(length/10):
            if stop == True:
                Lw.stop()
                Rw.stop()
                L_wheel = False
                R_wheel = False
            break
 
        wait(10)

    origin = [origin[0]+cos(radians(start_angle))*start[0]+sin(radians(start_angle))*start[1], origin[1]+sin(radians(start_angle))*start[0]+cos(radians(start_angle))*start[1], origin[2] + start[2], origin[3], origin[4]]
    return origin

        #print(L_angle, R_angle, "/", motor_angle)

#Aling functions
def align_line(speed, color, phases=4):
    """
    Four-phase alignment on the line of certain colour.

    Parameters:
        - speed: Number - deg/s (+ line is in front - line is behind)
        - color: {Color.COLOR - Color.WHITE, Color.NONE - (black)}
        - phases: Number - how many times may align
    """
    speed = -speed
    #speed is reflected in every phase, so if we want to start with positive speed we have to reflect it
    for i in range(phases):
        speed = -speed
        Lw.reset_angle(0)
        Rw.reset_angle(0)
        L_wheel = True
        R_wheel = True
        L_reverse = False
        R_reverse = False
        while True:
            L_angle = Lw.angle()
            R_angle = Rw.angle()
            L_col = Lc.color(True)
            R_col = Rc.color(True)
            L_speed = speed

            if i % 2 == 1:
                L_condition = L_col != color
                R_condition = R_col != color
            else:
                L_condition = L_col == color
                R_condition = R_col == color

            print(L_wheel, R_wheel, L_condition, R_condition, L_reverse, R_reverse)
            #motor corector
            R_speed = motor_corector(L_angle, R_angle, speed, extra_condition=L_wheel == True and L_reverse == False and R_reverse == False)

            if L_wheel == False and L_condition == False:
                print("L_reverse")
                L_reverse = True
                L_wheel = True
            if R_wheel == False and R_condition == False:
                print("R_reverse")
                R_reverse = True
                R_wheel = True
            if L_reverse == True:
                L_speed = -L_speed
            if R_reverse == True:
                R_speed = -R_speed

            #motor driver
            motor_driver(L_speed, R_speed, L_wheel, R_wheel)
            print(L_speed, R_speed, L_angle, R_angle)

            #motor breaker
            if L_condition:
                print("L", L_col)
                L_wheel = False
            if R_condition:
                print("R", R_col)
                R_wheel = False
            if L_condition and R_condition:
                if i == 1:
                    Lw.run_angle(speed, 45, then=Stop.HOLD, wait=False)
                    Rw.run_angle(speed, 45)
                Lw.stop()
                Rw.stop()
                break
    return None

def align_wall(speed, time, origin = [0, 0, 0, False, False]):
    """
    - nejsložitější jeď po nějakou dobu nějakou rychlostí.

    Parameters:
        - speed: Number - deg/s (+ forward, - backward)
        - time: Number - ms - how far the barrier is
    """
    timer = StopWatch()
    StopWatch.reset(timer)
    Lw.reset_angle(0)
    Rw.reset_angle(0)
    L_speed = speed

    while StopWatch.time(timer) <= time:
        L_angle = Lw.angle()
        R_angle = Rw.angle()
        avr_motor_angle = (L_angle + R_angle)/2
        angle = hub.imu.heading()
        origin = update_origin(origin, avr_motor_angle, angle)
        #motor corector
        R_speed = motor_corector(L_angle, R_angle, speed)

        Lw.run(L_speed)
        Rw.run(R_speed)
    Lw.stop()
    Rw.stop()
    return origin

def align_arm(arm, speed, stress=1):
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
    cons = abs(clamp(800/speed, 6, 1.5))*stress
    #cons(constant) = how many times the motor speed has to decrease to stop the motor.
    time = 300 + abs(speed/4)
    #time is time until the motor speeds up

    arm.run(speed)
    wait(time)

    while True:
        arm_speed = abs(arm.speed())
        #print(arm_speed, "/", speed)
        if arm_speed < abs(speed/cons):
            arm.stop()
            break

    return None

#composite functions
def calibrate_arm(speed: Number, arm=arm):
    align_arm(arm, speed)
    arm.reset_angle()
    align_arm(arm, -speed)
    max_angle = arm.angle()
    return max_angle

def ride(finish: list, radius: Number, origin: list, speed = default_speed):
    """
    tohle nefunguje!!!
    """
    x_shift = finish[0] - origin[0]
    y_shift = finish[1] - origin[1]
    length = sqrt(x_shift**2 + y_shift**2)*10
    radius = clamp(radius, abs(length/3), -abs(length/3))
    start_angle = degrees(atan2(y_shift, x_shift))
    angle_dif = start_angle - hub.imu.heading()
    
    origin = turn()
    origin = straight_position()
    return origin

def back_to_origin(origin):
    x = origin[0]
    y = origin[1]
    angle = degrees(atan2(y,x))
    distance = sqrt(x*x+y*y) * (-1)
    print(distance, angle)

    turn_2_g(angle, gyro_reset=False)
    straight_g(distance)
    turn_2_g(0, gyro_reset=False)

#system set up functions
def gandalf():
    while True:
        hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)

def victory_radar():
    radar_data = def_radar_data()
    while True:
        radar_data = radar_sken(radar_data)

def victory():
    hub.display.orientation(Side.LEFT)
    hub.display.icon(lime)
    while True:
        hub.speaker.play_notes(["A3/4", "R/4", "A3/8"], 130)
        UltraM.run(500)
        hub.speaker.play_notes(["A3/16", "A3/16", "A3/4", "R/4"], 130)
        UltraM.run(-500)
        hub.speaker.play_notes(["A3/8", "A3/16", "A3/16", "A3/4", "R/8"], 130)
        UltraM.run(500)
        hub.speaker.play_notes(["C4/4", "A3/8", "R/8", "G3/8"], 130)
        UltraM.run(-500)
        hub.speaker.play_notes(["G3/8", "F3/8", "R/8", "D3/8", "D3/8"], 130)
        UltraM.run(500)
        hub.speaker.play_notes([ "E3/8", "F3/8", "D3/8"], 130)
        UltraM.run(-500)