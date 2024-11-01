from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.tools import wait, StopWatch, multitask, run_task
from icons import*
from umath import*

### Mathematical function
def clamp(value: float, maximum: float, minimum: float):
    """
    keeps the value between maximum and minimum

    Parameters:
        - value: float
        - maximum: float
        - minimum: float

    Returns:
        - value between maximum and minimum
    """
    if maximum >= value >= minimum:
        final_value = value
    elif maximum < value:
        final_value = maximum
    elif minimum > value:
        final_value = minimum
    return(final_value)

def absclamp(value: float, maximum: float, minimum: float):
    """
    keeps absolute value of the value between maximum and minimum

    Parameters:
        - value: float
        - maximum: float
        - minimum: float

    Returns:
        - value float
    """
    maximum = abs(maximum)
    minimum = abs(minimum)
    if maximum >= abs(value) >= minimum:
        final_value = value
    elif value == 0:
        final_value = 0
    elif maximum < abs(value):
        final_value = maximum*value/abs(value)
    elif minimum > abs(value):
        final_value = minimum*value/abs(value)
    return(final_value)

def motor_corector(L_angle, R_angle, speed, ratio: Number=1, extra_condition=True):#not shure how useful
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

# Whatever
class Robot:
    def __init__(self,
        hub: PrimeHub, 
        wheel_radius: float, 
        axle_track: float, 
        left_wheel: Motor, 
        right_wheel: Motor, 
        deaful_speed: int = 900, 
        acceleration: float = 1, 
        deceleration: float = 1, 
        gear: float = 1):
        """
        Parameters:
            - wheel_radius: float ... in mm
            - axle_track: float ... in mm
            - left_wheel: Motor ... name
            - right_wheel: Motor ... name
            - deaful_speed: int ... in deg/s
            - acceleration: float ... in rot
            - deceleration: float ... in rot
            - gear: float ... (wheel rot/motor rot)
        """
        self.wheel_radius = wheel_radius
        self.onerot = 2 * pi * wheel_radius * gear
        self.axle_track = axle_track

        self.hub = hub
        self.Lw = left_wheel
        self.Rw = right_wheel

        self.deaful_speed = deaful_speed
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.gear = gear

        #probably useless
        self.x = 0
        self.y = 0
        self.Lw_angle = 0
        self.Rw_angle = 0
        self.avr_motor_angle = 0
        self.orientation = 0
        self.status_skip = False
  
    def add_ultrasonic(self, sensor: UltrasonicSensor):#
        self.ultrasonic = sensor

    def add_touch(self, sensor: ForceSensor):#
        self.touch = sensor

    def add_color(self, sensor: ColorSensor):#
        self.color = sensor

    def add_motor(self, motor: Motor):#
        self.motor = motor

    def set_origin(self, x: float, y: float, orientation: float, field_range: list = [[0,0],[0,0]]):
        """
        Paprameters:
            - x: float ... in mm
            - y: float ... in mm
            - orientation: float ... in deg
        """
        self.x = x
        self.y = y
        self.orientation_dif = self.hub.imu.heading() - orientation
        print(self.orientation_dif)
        self.field = field_range
        self.Lw.reset_angle(0)
        self.Rw.reset_angle(0)

    def set_local_origin(self, x: float, y: float, orientation: float):
        """
        determins local/sub-origin for functions
        Parameters:
            - x: float ... in mm
            - y: float ... in mm
            - orientation: float ... in deg
        """
        self.local_initial_Lw_angle = self.Lw.angle()
        self.local_initial_Rw_angle = self.Rw.angle()
        self.local_x = x
        self.local_y = y
        self.local_orientation_dif = orientation
        
    def checkpoint(self, x: float, y: float):###
        """
        Parameters
        """
        self.x = x
        self.y = y

    def get_orientation(self):
        """
        replacement for self.hub.imu.heading()
        """
        self.orientation = self.hub.imu.heading() - self.orientation_dif

    def accelerator(
        self,
        actual_motor_angle: float, 
        motor_angle: float, 
        speed: int, 
        min_speed: int = 50,
        initial_speed: int = 50,
        terminal_speed: int = 50
        ):
        """
        - This function works with the robot's speed and modifies it for a smooth start and stop.
        - This function is designed for being part of a loop.
        - It's recomentded to place this before motor corector.
        - This function could cause slower reactions of robot.

        Parameters:
            - actual_motor_angle: float ... in deg ... mesured motor angle, if you work with 2 motor movement, place here average angle of both motors.
            - motor_angle: float ... in deg ... AIM angle
            - speed: int ... in deg/s ... raw speed
            - min_speed: int ... in deg/s

        uses: calmp, absclamp
        """
        
        acceleration = self.acceleration
        deceleration = self.deceleration

        if deceleration == 0 or motor_angle == 0:
            max_speed = speed
        else:
            max_speed = absclamp((motor_angle - actual_motor_angle)/(deceleration*0.36), speed, terminal_speed)

        if acceleration == 0:
            new_speed = max_speed
        else:
            new_speed = absclamp((actual_motor_angle/(acceleration*3.6))**2 + abs(initial_speed) + min_speed, max_speed, min_speed)

        if motor_angle != 0:
            new_speed = new_speed * motor_angle / abs(motor_angle)

        return new_speed

    def locate(self, local: bool = False):
        pavr_motor_angle = self.avr_motor_angle
        self.Lw_angle = self.Lw.angle()
        self.Rw_angle = self.Rw.angle()
        self.avr_motor_angle = (self.Lw_angle + self.Rw_angle)/2
        self.get_orientation()
        
        #if abs(pavr_motor_angle) - 100 > abs(self.avr_motor_angle):
        #    motor_dif = self.avr_motor_angle
        #else:

        distance = ((self.avr_motor_angle - pavr_motor_angle)/360)*self.onerot
        #print(La.angle(), Ra.angle(), distance)
        #print(sin(alfa), cos(alfa))
        angle = radians(self.orientation)
        self.x = self.x + cos(angle) * distance
        self.y = self.y + sin(angle) * distance

        if local:
            self.local_orientation = self.orientation - self.local_orientation_dif
            self.local_Lw_angle = self.Lw_angle - self.local_initial_Lw_angle
            self.local_Rw_angle = self.Rw_angle - self.local_initial_Rw_angle
            self.local_avr_motor_angle = (self.local_Lw_angle + self.local_Rw_angle)/2
            angle = radians(self.local_orientation)
            self.local_x = self.local_x + cos(angle) * distance
            self.local_y = self.local_y + sin(angle) * distance 

    def pressme(self, on: bool, color: Color = Color.CYAN):
        """
        highlights central button

        Parameters:
            on: Logic (True - highlight, False - turn light off)
        """
        if on == True:
            self.hub.light.blink(color, [500, 50, 200, 50])
        else:
            self.hub.light.on(color)

    def motor_driver(self, L_speed: float, R_speed: float, L_wheel: bool, R_wheel: bool):
        """
        - this function turns of motor based on logic imput

        Parameters
            - L_speed: Number - deg/s
            - R_speed: Number - deg/s
            - L_wheel: Logic
            - R_wheel: Logic
        """
        if L_wheel == True:
            self.Lw.run(L_speed)
        else:
            self.Lw.brake()
        if R_wheel == True:
            self.Rw.run(R_speed)
        else:
            self.Rw.brake()

    def straight_g(self, distance: float, terminal_speed: int = 50, set_angle: bool = False, angle: float = 0, skippable: bool = False, speed: Oprional[float] = None):
        """
        extra precise straight movement
        
        Parameters:
            - distance: Number - in mm
            - speed: Number - in deg/s
            - origin: list
            - terminal_speed: Number - in deg/s
            - set_angle: bool
            - angle: Number - in deg
        
        uses: accelerator, motor_controler, motor_driver, clamp, absclamp
        """
        if skippable and self.status_skip:
            return None

        time = 10
        g_cons = 20
        corector_cons = 10
        #gyroconstant

        self.get_orientation()
        L_wheel = True
        R_wheel = True
        motor_angle = (distance*360/self.onerot)
        L_speed = self.Lw.speed(window=10)
        R_speed = self.Rw.speed(window=10)
        avr_initial_speed = (L_speed + R_speed)/2

        if speed == None:
            speed = self.deaful_speed
        else:
            speed = speed

        if set_angle == False:
            start_angle = self.orientation
        else:
            start_angle = angle

        self.set_local_origin(0, 0, start_angle)

        terminal_speed = clamp(terminal_speed, 900, 50)
        if terminal_speed == 50:
            stop = True
        else:
            stop = False
        
        while True:       
            self.locate(local=True)

            #print(L_angle, R_angle)
            new_speed = self.accelerator(self.local_avr_motor_angle, motor_angle, speed, initial_speed=avr_initial_speed, terminal_speed=terminal_speed)

            #print(new_speed, ";", start[0], ";", finish[0])
            gyro_corection = self.local_orientation * g_cons
            shift_corection = self.local_y * corector_cons
            L_speed = new_speed - gyro_corection - shift_corection
            R_speed = new_speed + gyro_corection + shift_corection

            #print(L_speed, R_speed)

            self.motor_driver(L_speed, R_speed, L_wheel, R_wheel)

            #motor breaker
            if abs(self.local_x) > abs(distance):
                #print("vypínač")
                if stop == True:
                    self.Lw.stop()
                    self.Rw.stop()
                    L_wheel = False
                    R_wheel = False
                break
            #wait(10)

    def straight_position(self, x, y, direction: int, terminal_speed: Number = 50, skippable: bool = False, speed: Oprional[float] = None):
        """
        extra precise straight movement
        
        Parameters:
            - finish: list [x, y] - in mm
            - direction: int
            - speed: Number - in deg/s
            - terminal_speed: Number - in deg/s
        
        uses: accelerator, motor_controler, motor_driver, clamp, absclamp
        """

        if skippable and self.status_skip:
            return None

        if self.field[0][0] - self.field[1][0] != 0:
            x = (x - self.field[0][0]) % abs(self.field[0][0]- self.field[1][0]) + self.field[0][0]
        if self.field[0][1] - self.field[1][1] != 0:
            y = (y - self.field[0][1]) % abs(self.field[0][1]- self.field[1][1]) + self.field[0][1]
        print(x,y)
        #constants
        time = 10
        g_cons = 20
        corector_cons = 10 * direction

        #trajectory calculator
        direction = absclamp(direction, 1, 1)
        x_shift = (x - self.x)*direction
        y_shift = (y - self.y)*direction
        distance = sqrt(x_shift**2 + y_shift**2)*direction
        print(x_shift, y_shift, distance)

        if distance == 0:
            print("start=cíl")
            return None 

        #setup
        self.get_orientation()
        L_wheel = True
        R_wheel = True
        motor_angle = (distance*360/self.onerot)
        L_speed = self.Lw.speed(window=10)
        R_speed = self.Rw.speed(window=10)
        avr_initial_speed = (L_speed + R_speed)/2
        terminal_speed = clamp(terminal_speed, 900, 50)
        start_angle = degrees(atan2(y_shift, x_shift))

        if start_angle - self.orientation > 180:
            start_angle -= 360
        elif start_angle - self.orientation < -180:
            start_angle += 360

        self.set_local_origin(0, 0, start_angle)

        if speed == None:
            speed = self.deaful_speed
        else:
            speed = speed

        if terminal_speed == 50:
            stop = True
        else:
            stop = False
        
        while True:       
            self.locate(local=True)

            new_speed = self.accelerator(self.local_avr_motor_angle, motor_angle, speed, initial_speed=avr_initial_speed, terminal_speed=terminal_speed)
            gyro_corection = self.local_orientation * g_cons
            shift_corection = self.local_y * corector_cons
            L_speed = new_speed - gyro_corection - shift_corection
            R_speed = new_speed + gyro_corection + shift_corection

            self.motor_driver(L_speed, R_speed, L_wheel, R_wheel)

            #motor breaker
            if abs(self.local_x) > abs(distance):
                #print("vypínač")
                if stop == True:
                    self.Lw.stop()
                    self.Rw.stop()
                    L_wheel = False
                    R_wheel = False
                break

    def turn(self, angle: float, radius: float, stop: bool=True, skippable: bool = False, speed: Oprional[float] = None, gyro_use: bool=True, gyro_reset: bool=False):
        """
        Parameters:
            - angle: float - in deg - positive = clockwise, negative = counterclockwise, 0 = nowhere
            - radius: float - in mm - positive = left, negative = right, 0 = on site, Robot_name.onerot/2 = by one wheel 
            - stop: bool - than stop or not?
            - skippable: bool - if True, it'll be skipped
            - gyro_use: bool - do you want to use gyro? (yes you want, everybody wants)
            - gyro_reset: bool - reset gyro or not?
            - speed: Number - in deg/s - it's recommended to slow down if the radius is too small
        """
        #angle corector
        if skippable and self.status_skip:
            return None

        self.get_orientation()
        if gyro_reset == True:
            start_angle = self.orientation
            motor_initial_angle = 0
        else:
            start_angle = 0
            motor_initial_angle = self.orientation

        if speed == None:
            speed = self.deaful_speed
        else:
            speed = speed
        
        #speed calculator
        if radius >= 0:
            Rw_ratio = clamp((radius - self.axle_track/2)/abs(radius + self.axle_track/2), 1, -1)
        else:
            Rw_ratio = -1
        if radius <= 0:
            Lw_ratio = clamp((radius + self.axle_track/2)/abs(radius - self.axle_track/2), 1, -1)
        else:
            Lw_ratio = 1
        #print(Lw_ratio, Rw_ratio, Lw_ratio*Rw_ratio)

        #setup
        cons = clamp(4000/speed + abs(radius)/10 ,50,5)
        trajectory = (abs(radius) + self.axle_track)*pi
        motor_angle = (trajectory/self.onerot) * (angle - motor_initial_angle)
        ### motor angle calculaton concept not vetrified not vetrified
        
        if gyro_use == True:
            gyro_error = False
        else:
            gyro_error = True

        #motor setup
        self.set_local_origin(0, 0, 0)
        L_speed = self.Lw.speed(window=10)
        R_speed = self.Rw.speed(window=10)
        avr_initial_speed = (L_speed + R_speed)/2

        #main loop
        while True:
            #reeder
            self.locate(True)
            angle_dif = angle - self.orientation
            
            abs_motor_angle = abs(self.local_Lw_angle) + abs(self.local_Rw_angle)
            new_speed = self.accelerator(abs_motor_angle, 0, speed, initial_speed=avr_initial_speed)
            #print(self.orientation, angle_dif)
            #core
            if gyro_error == False:

                #speed calculator
                
                if stop == True:
                    motor_speed = absclamp(angle_dif*cons, new_speed, 2)
                else:
                    motor_speed = speed * angle_dif/abs(angle_dif)
                #print(motor_speed)

                #motor driver
                self.Lw.run(motor_speed * Lw_ratio)
                self.Rw.run(motor_speed * Rw_ratio)

                #print(actual_angle, "/",angle)

                #motor braker
                if abs(abs(angle)-abs(self.orientation))<=1:
                    #print("done")
                    if stop == True:
                        self.Lw.brake()
                        self.Rw.brake()
                    break

                #check
                if abs(abs_motor_angle) > abs(motor_angle) + 3600:
                    #print(L_motor_angle, "/", motor_angle)
                    for i in range(4):
                        self.hub.speaker.beep(500, 50)
                        wait(50)
                    gyro_error = True
                    stop = True

            #error
            else:
                if stop == True:
                    L_motor_speed = absclamp((motor_angle - L_motor_angle) * cons, new_speed, 5)
                    #taky špatně
                else:
                    L_motor_speed = new_speed
                
                #motor controler
                R_motor_speed = motor_corector(L_motor_angle, R_motor_angle, L_motor_speed)
                #nemme L_angle a R_angle
            
                self.Lw.run(L_motor_speed * Lw_ratio)
                self.Rw.run(R_motor_speed * Rw_ratio)

                #break
                if (abs(L_motor_angle) + abs(R_motor_angle)) / 2 > motor_angle:
                    self.Lw.stop()
                    self.Rw.stop()
                    break
        
        return

    