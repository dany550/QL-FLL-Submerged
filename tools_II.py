from pybricks.hubs import*
from pybricks.pupdevices import*
from pybricks.parameters import*
from pybricks.tools import*
from icons import*
from umath import*

from mathClasses import*


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
        self.motor = WheelMotor(left_wheel,right_wheel)

        self.deaful_speed = deaful_speed
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.gear = gear

        #probably useless
        self.pos = Vec(0,0)
        self.angle = Angle(0,0,self.motor)
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

    def set_origin(self, x: float, y: float, orientation: float):
        """
        Paprameters:
            - x: float ... in mm
            - y: float ... in mm
            - orientation: float ... in deg
        """
        self.x = x
        self.y = y
        self.orientation_dif = orientation - self.hub.imu.heading()
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
        # nazdar tome
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
        self.angle.Update()
        self.avr_motor_angle = (self.angle.L + self.angle.R)/2
        self.get_orientation()

        distance = ((self.avr_motor_angle - pavr_motor_angle)/360)*self.onerot
        angle = radians(self.orientation)
        self.pos += Vec(cos(angle) * distance,sin(angle) * distance)

        #if local:
        #    self.local_orientation = self.orientation - self.local_orientation_dif
        #    self.localAngle.L -= self.local_initial_Lw_angle
        #    self.localAngle.R -= self.local_initial_Rw_angle
        #    self.local_avr_motor_angle = (self.local_Lw_angle + self.local_Rw_angle)/2
        #    angle = radians(self.local_orientation)
        #    self.local_x = self.local_x + cos(angle) * distance
        #    self.local_y = self.local_y + sin(angle) * distance 

    def pressme(self, on: bool, color: Color = Color.CYAN):
        """
        highlights central button

        padající trubka

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
            self.motor.L.run(L_speed)
        else:
            self.motor.L.brake()
        if R_wheel == True:
            self.motor.R.run(R_speed)
        else:
            self.motor.R.brake()

    def straight_g(self, distance: float, terminal_speed: int = 50, set_angle: bool = False, angle: float = 0, skippable: bool = False, speed: Optional[float] = None):
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

        self.get_orientation()
        motor_angle = (distance*360/self.onerot)
        L_speed = self.motor.L.speed(window=10)
        R_speed = self.motor.R.speed(window=10)
        avr_initial_speed = Avg([R_speed,L_speed])

        L_wheel = True
        R_wheel = True

        if speed == None:
            speed = self.deaful_speed

        if set_angle == False:
            angle = self.orientation

        initPos = Vec(self.pos.x,self.pos.y)
        rotMat = Matrix.rot(radians(angle))

        terminal_speed = clamp(terminal_speed, 900, 50)
        stop = False
        if terminal_speed == 50:
            stop = True
        
        lastAngle = Angle(self.angle.x,self.angle.y)
        deltaAngle = 0
        
        lastOri = self.orientation
        
        while True:       
            self.locate()
            deltaAngle = Angle(self.angle.L - lastAngle.L,self.angle.R - lastAngle.R)

            localPos = rotMat * (self.pos-initPos)
            new_speed = self.accelerator(Avg(deltaAngle), motor_angle, speed, initial_speed=avr_initial_speed, terminal_speed=terminal_speed)
            
            gyro_corection = (self.orientation-lastOri) * g_cons
            shift_corection = localPos.y * corector_cons
            L_speed = new_speed - gyro_corection - shift_corection
            R_speed = new_speed + gyro_corection + shift_corection

            self.motor_driver(L_speed, R_speed, True, True)

            #motor breaker
            if abs(localPos.x) > abs(distance):
                if stop == True:
                    self.motor.L.stop()
                    self.motor.R.stop()
                    L_wheel = False
                    R_wheel = False
                break

    def straight_position(self, pos: Vec, direction: int, terminal_speed: Number = 50, skippable: bool = False, speed: Optional[float] = None):
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

        #constants
        time = 10
        g_cons = 20
        corector_cons = 10 * direction

        #trajectory calculator
        direction = absclamp(direction, 1, 1)
        
        shift = (pos - self.pos) * direction
        distance = shift.lenght() * direction

        if distance == 0:
            print("start=cíl")
            return None 

        #setup
        self.get_orientation()
        L_wheel = True
        R_wheel = True
        motor_angle = (distance*360/self.onerot)
        L_speed = self.motor.L.speed(window=10)
        R_speed = self.motor.R.speed(window=10)
        avr_initial_speed = Avg([L_speed,R_speed])
        terminal_speed = clamp(terminal_speed, 900, 50)
        start_angle = degrees(atan2(shift.y, shift.x))

        self.set_local_origin(0, 0, start_angle)
        
        initPos = Vec(self.pos.x,self.pos.y)
        rotMat = Matrix(-start_angle)
        
        
        if speed == None:
            speed = self.deaful_speed
        stop = False
        if terminal_speed == 50:
            stop = True
        
        lastAngle = Angle(self.angle.x,self.angle.y)
        deltaAngle = 0
        
        lastOri = self.orientation
        
        while True:
            
            self.locate()
            deltaAngle = Angle(self.angle.L - lastAngle.L,self.angle.R - lastAngle.R)

            localPos = rotMat * (self.pos-initPos)
            
            new_speed = self.accelerator(Avg(deltaAngle), motor_angle, speed, initial_speed=avr_initial_speed, terminal_speed=terminal_speed)
            gyro_corection = (self.orientation - lastOri) * g_cons
            shift_corection = localPos.y * corector_cons
            L_speed = new_speed - gyro_corection - shift_corection
            R_speed = new_speed + gyro_corection + shift_corection

            self.motor_driver(L_speed, R_speed, L_wheel, R_wheel)

            #motor breaker
            if abs(localPos.x) > abs(distance):
                if stop == True:
                    self.motor.L.stop()
                    self.motor.R.stop()
                    L_wheel = False
                    R_wheel = False
                break

    def turn(self, angle: float, radius: float, stop: bool=True, skippable: bool = False, speed: Optional[float] = None, gyro_use: bool=True, gyro_reset: bool=False):
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


def testttt(*values: object, N: int):
    print(values)
    print(N)