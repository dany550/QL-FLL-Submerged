from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon, Axis
from pybricks.tools import wait, StopWatch, multitask, run_task
from icons import*
from umath import*

### Mathematical function
def sign(value: float, zero: bool = True):
    if value == 0 and zero:
        sign = 0
    elif value < 0:
        sign = -1
    else:
        sign = 1
    return sign

def avrg(*value: float):
    avrg = sum(value)/len(value)
    return avrg

def angle_mod(value: float):
    value = (value + 180) % 360 - 180
    return value

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
    return final_value

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
    vsign = sign(value)
    if maximum >= abs(value) >= minimum:
        final_value = value
    elif value == 0:
        final_value = 0
    elif maximum < abs(value):
        final_value = maximum*vsign
    elif minimum > abs(value):
        final_value = minimum*vsign
    return final_value

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
class Arm(Motor):
    def __init__(self, port: Port, positive_direction: Direction=Direction.CLOCKWISE, gears: Optional[Union[Collection[int], Collection[Collection[int]]]]=None, reset_angle: bool=True, profile: Number=None, stress: float =1):
        """
        this is expaniso for motor class

        Parameters:
            - port: Port Port to which the motor is connected. 
            - positive_direction: Direction Which direction the motor should turn when you give a positive speed value or angle. 
            - gears: list List of gears linked to the motor. The gear connected to the motor comes first and the gear connected to the output comes last.
                For example: ``[12, 36]`` represents a gear train with a
                12-tooth gear connected to the motor and a 36-tooth gear
                connected to the output. Use a list of lists for multiple
                gear trains, such as ``[[12, 36], [20, 16, 40]]``.
                When you specify a gear train, all motor commands and settings
                are automatically adjusted to account for the resulting gear
                ratio. The motor direction remains unchanged by this.
            - reset_angle: bool Choose True to reset the rotation sensor value to the absolute marker angle (between -180 and 179). Choose False to keep the current value, so your program knows where it left off last time. 
            - profile: Number, deg Precision profile. This is the approximate position tolerance in degrees that is acceptable in your application. A lower value gives more precise but more erratic movement; a higher value gives less precise but smoother movement. If no value is given, a suitable profile for this motor type will be selected automatically (about 11 degrees).
            - stress: float
        """
        super().__init__(port, positive_direction, gears, reset_angle, profile)
        self.stress = clamp(abs(stress), 8, 0.25)
    
    def align(self, speed):
        """
        stops the motor as soon as it meets resistance

        Parameters:
            - speed: Number - deg/s (+ clockwise, - counterclockwise)
            - stress: Number - if the motor is under upnormal stress, change stress <0.25; 8>. More stress means higher resistence of motor.
        """
        #limiter
        speed = clamp(abs(speed), 1000, 100)*sign(speed) 
        self.stress = clamp(abs(self.stress), 8, 0.25)
        cons = abs(clamp(800/speed, 6, 1.5))*self.stress
        #cons(constant) = how many times the motor speed has to decrease to stop the motor.
        time = 300 + abs(speed/4)
        #time is time until the motor speeds up

        self.run(speed)
        wait(time)

        while True:
            arm_speed = abs(self.speed())
            #print(arm_speed, "/", speed)
            if arm_speed < abs(speed/cons):
                self.stop()
                break

class Ultrasonic(UltrasonicSensor):
    def __init__(self, port: Port, x_shift: float, y_shift: float, orientation: float):
        """
        this is expansion of UltrasonicSensor class designed of locating

        Parameters:
            - port: Port ... Port to which the sensor is connected.
            - x_shift: float
            - y_shift: float
            - orientation: float
        """
        super(UltrasonicSensor).__init__(port)
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.orientation = orientation

class Robot:
    #setup funcrions
    def __init__(self,
        hub: PrimeHub, 
        wheel_radius: float, 
        axle_track: float, 
        left_wheel: Motor, 
        right_wheel: Motor, 
        deaful_speed: int = 900, 
        acceleration: float = 1, 
        deceleration: float = 1, 
        gear: float = 1,
        extra_task: object = None):
        """
        Parameters:
            - wheel_radius: float ... in mm
            - axle_track: float ... in mm
            - left_wheel: Motor ... name
            - right_wheel: Motor ... name
            - deaful_speed: int ... in deg/s
            - acceleration: float ... in rot
            - deceleration: float ... in rot
            - gear: float ... (wheel rot/motor rot) #may be improved...
        
        # could be rewriten to drivebase extension
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

        #constants
        

        #probably useless
        self.x = 0
        self.y = 0
        self.Lw_angle = 0
        self.Rw_angle = 0
        self.avr_motor_angle = 0
        self.orientation = 0
        self.status_skip = False
        self.interupt = False

        self.extra_task = extra_task

    def add_arms(self, *arm: Arm):
        self.arms = arm

    def set_origin(self, x: float, y: float, orientation: float, field_range: list = [[0,0],[0,0]]):
        """
        Paprameters:
            - x: float ... in mm
            - y: float ... in mm
            - orientation: float ... in deg
        """
        self.x = x
        self.y = y
        self.orientation_dif = orientation - self.hub.imu.heading()
        self.field = field_range
        self.Lw.reset_angle(0)
        self.Rw.reset_angle(0)

    def set_local_origin(self, x: float, y: float, orientation: float, window: int = 10):
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
        self.avr_initial_speed = avrg(self.Lw.speed(window=window), self.Rw.speed(window=window))
    
    #looppart functions
    def get_orientation(self):
        """
        replacement for self.hub.imu.heading()
        """
        self.orientation = self.orientation_dif - self.hub.imu.heading()
        return self.orientation

    def get_acceleration(self):
        self.acceleration = self.hub.imu.acceleration(Axis.Y)

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
            max_speed = absclamp((motor_angle - actual_motor_angle)/(deceleration*0.36), speed, terminal_speed) #0.36 = 360/1000; 1000 = max speed

        if acceleration == 0:
            new_speed = max_speed
        else:
            new_speed = absclamp((actual_motor_angle/(acceleration*3.6))**2 + abs(initial_speed) + min_speed, max_speed, min_speed)

        new_speed = new_speed * sign(motor_angle)

        return new_speed

    def speed_calculator(self, motor_angle, speed, terminal_speed, g_cons, corector_cons):
        new_speed = self.accelerator(self.local_avr_motor_angle, motor_angle, speed, initial_speed=self.avr_initial_speed, terminal_speed=terminal_speed)
        gyro_corection = self.local_orientation * g_cons
        shift_corection = self.local_y * corector_cons
        self.L_speed = new_speed + gyro_corection + shift_corection
        self.R_speed = new_speed - gyro_corection - shift_corection  
        #print(new_speed, ";", self.L_speed, ";", self.R_speed)

    def locate(self, local: bool = False):
        """
        # accelerometric check might be added (because of big accelerometric uncertanty it'll by recognizing unfortunate deccelerations)
        """
        pavr_motor_angle = self.avr_motor_angle
        self.Lw_angle = self.Lw.angle()
        self.Rw_angle = self.Rw.angle()
        self.avr_motor_angle = avrg(self.Lw_angle, self.Rw_angle)
        self.get_orientation()
        
        #if abs(pavr_motor_angle) - 100 > abs(self.avr_motor_angle):
        #    motor_dif = self.avr_motor_angle
        #else:

        distance = ((self.avr_motor_angle - pavr_motor_angle)/360)*self.onerot
        #print(La.angle(), Ra.angle(), distance)
        #print(sin(alfa), cos(alfa))
        angle = radians(self.orientation)
        self.x += cos(angle) * distance
        self.y += sin(angle) * distance

        if local:
            self.local_orientation = self.orientation - self.local_orientation_dif
            self.local_Lw_angle = self.Lw_angle - self.local_initial_Lw_angle
            self.local_Rw_angle = self.Rw_angle - self.local_initial_Rw_angle
            self.local_avr_motor_angle = avrg(self.local_Lw_angle, self.local_Rw_angle)
            angle = radians(self.local_orientation)
            self.local_x += cos(angle) * distance
            self.local_y += sin(angle) * distance 

    def motor_driver(self, L_speed: float, R_speed: float):
        """
        - this function turns of motor based on logic imput

        Parameters
            - L_speed: Number - deg/s
            - R_speed: Number - deg/s
        """
        self.Lw.run(L_speed)
        self.Rw.run(R_speed)

    def motor_braker(self, stop):
        if stop:
            self.Lw.brake()
            self.Rw.brake()

    #instant functions
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

    #complex motion functions
    def straight_g(self, distance: float, terminal_speed: int = 50, set_angle: bool = False, angle: float = 0, skippable: bool = False, speed: Oprional[float] = None, task: object = None):
        """
        extra precise straight movement
        
        Parameters:
            - distance: Number - in mm
            - speed: Number - in deg/s
            - origin: list
            - terminal_speed: Number - in deg/s
            - set_angle: bool
            - angle: Number - in deg
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        
        uses: accelerator, motor_controler, motor_driver, clamp, absclamp
        """
        if skippable and self.status_skip:
            return None

        g_cons = 20 # gyrocorector constant
        corector_cons = 10 * sign(distance) # shiftcorector constant
        motor_angle = (distance*360/self.onerot)
        terminal_speed = clamp(terminal_speed, 900, 50)
        stop = terminal_speed == 50
        if speed == None:
            speed = self.deaful_speed

        self.get_orientation()
        if set_angle == False:
            start_angle = self.orientation
        else:
            start_angle = angle
        self.set_local_origin(0, 0, start_angle)
        
        while True:
            self.locate(local=True)
            self.speed_calculator(motor_angle, speed, terminal_speed, g_cons, corector_cons)
            self.motor_driver(self.L_speed, self.R_speed)

            if task:
                task()
            if self.extra_task:
                self.extra_task()

            #motor breaker
            if abs(self.local_x) > abs(distance) or self.interupt:
                self.motor_braker(stop)
                break
           
    def straight_position(self, x: float, y: float, direction: int, terminal_speed: Number = 50, skippable: bool = False, speed: Oprional[float] = None, task: object = None):
        """
        extra precise straight movement
        
        Parameters:
            - x: float
            - y: float
            - direction: int
            - terminal_speed: Number - in deg/s
            - skippable: bool
            - speed: Number - in deg/s
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        
        uses: accelerator, motor_controler, motor_driver, clamp, absclamp
        """

        if skippable and self.status_skip:
            return None

        #setup
        g_cons = 20 # gyrocorector constant (its not recomended to set below 2 and above 50)
        corector_cons = 10 * direction
        if speed == None: #may be modified
            speed = self.deaful_speed
        terminal_speed = clamp(terminal_speed, 1000, 50)
        stop = terminal_speed == 50
        start_angle = self.get_orientation()
        if self.field[0][0] - self.field[1][0] != 0: # to incorporate matrix magic
            x = (x - self.field[0][0]) % abs(self.field[0][0]- self.field[1][0]) + self.field[0][0]
        if self.field[0][1] - self.field[1][1] != 0:
            y = (y - self.field[0][1]) % abs(self.field[0][1]- self.field[1][1]) + self.field[0][1]
        direction = clamp(direction, 1, -1)
        x_shift = (x - self.x)*direction
        y_shift = (y - self.y)
        print(self.x, self.y, x_shift, y_shift)
        
        #trajectory calculator
        track_angle = angle_mod(degrees(atan2(y_shift, x_shift)))
        #if direction == 0:
        #    direction = sign(90 - abs(angle_mod(track_angle - start_angle)), zero=False)
        track_angle = track_angle * direction
        distance = sqrt(x_shift**2 + y_shift**2)*direction
        if distance == 0:
            print("start=cíl")
            return None 
        motor_angle = (distance*360/self.onerot)
        self.set_local_origin(0, 0, track_angle)

        while True:
            self.locate(local=True)
            self.speed_calculator(motor_angle, speed, terminal_speed, g_cons, corector_cons)
            self.motor_driver(self.L_speed, self.R_speed)

            if task:
                task()
            if self.extra_task:
                self.extra_task()

            #motor breaker
            if abs(self.local_x) > abs(distance) or self.interupt: 
                self.motor_braker(stop)
                break

    def turn(self, angle: float, radius: float, terminal_speed: int = 50, skippable: bool = False, speed: Oprional[float] = None, gyro_reset: bool=False, task: object = None):
        """
        check might be added (by use of abs avr actual motor angle)
        ### to update description
        Parameters:
            - angle: float - in deg - positive = clockwise, negative = counterclockwise, 0 = nowhere
            - radius: float - in mm - positive = left, negative = right, 0 = on site, Robot_name.onerot/2 = by one wheel 
            - skippable: bool - if True, it'll be skipped
            - gyro_use: bool - do you want to use gyro? (yes you want, everybody wants)
            - gyro_reset: bool - reset gyro or not?
            - speed: Number - in deg/s - it's recommended to slow down if the radius is too small
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        """
        if skippable and self.status_skip:
            return None

        if gyro_reset:
            start_angle = 0
        else:
            start_angle = self.get_orientation()
        terminal_speed = clamp(terminal_speed, 1000, 50)
        stop = terminal_speed == 50
        #angle = angle_mod(angle)
        ori_diff = angle - start_angle #in deg
        motor_angle = (abs(radius) + self.axle_track) * pi * ori_diff / self.onerot #average absolute trajectory in deg
        self.set_local_origin(0, 0, start_angle)

        #speed calculator
        if radius >= 0:
            Lw_ratio = clamp((radius - self.axle_track/2)/abs(radius + self.axle_track/2), 1, -1)
        else:
            Lw_ratio = -1
        if radius <= 0:
            Rw_ratio = clamp((radius + self.axle_track/2)/abs(radius - self.axle_track/2), 1, -1)
        else:
            Rw_ratio = 1
        if speed == None:
            speed = self.deaful_speed
        #print(Lw_ratio, Rw_ratio, Lw_ratio*Rw_ratio)

        while True:
            self.locate(True)
            actual_motor_angle = (abs(radius) + self.axle_track) * pi * self.local_orientation / self.onerot #average absolute trajectory in deg
            motor_speed = self.accelerator(actual_motor_angle, motor_angle, speed, 50, self.avr_initial_speed, terminal_speed)
            self.motor_driver(motor_speed * Lw_ratio, motor_speed * Rw_ratio)
            #print(motor_angle, ";", actual_motor_angle)

            if task:
                task()
            if self.extra_task:
                self.extra_task()

            #motor braker
            if abs(abs(angle)-abs(self.orientation))<=1:
                if stop:
                    self.motor_braker(stop)
                break

    def get_to(self, x: float, y: float , orientation: float, terminal_speed: Number = 50, skippable: bool = False, speed: Oprional[float] = None, task: object = None):
        """
        to be developed...
        extra precise straight movement
        
        Parameters:
            - x: float
            - y: float
            - direction: int
            - terminal_speed: Number - in deg/s
            - skippable: bool
            - speed: Number - in deg/s
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        
        uses: accelerator, motor_controler, motor_driver, clamp, absclamp
        """
        if skippable and self.status_skip:
            return None

        #setup
        g_cons = 20 # gyrocorector constant (its not recomended to set below 2 and above 50)
        corector_cons = 10
        if speed == None: #may be modified
            speed = self.deaful_speed
        terminal_speed = clamp(terminal_speed, 1000, 50)
        stop = terminal_speed == 50
        start_angle = self.get_orientation()
        aim_angle = angle_mod(orientation)
        if self.field[0][0] - self.field[1][0] != 0: # to incorporate matrix magic
            x = (x - self.field[0][0]) % abs(self.field[0][0]- self.field[1][0]) + self.field[0][0]
        if self.field[0][1] - self.field[1][1] != 0:
            y = (y - self.field[0][1]) % abs(self.field[0][1]- self.field[1][1]) + self.field[0][1]
        x_shift = x - self.x
        y_shift = y - self.y
        
        #trajectory calculator
        track_angle = angle_mod(degrees(atan2(y_shift, x_shift)))
        ori_diff = abs(angle_mod(track_angle - start_angle) + angle_mod(track_angle - aim_angle))
        direction = sign(180 - ori_diff, zero=False)
        track_angle = track_angle * direction
        distance = sqrt(x_shift**2 + y_shift**2)*direction
        if distance == 0:
            print("start=cíl")
            return None 
        motor_angle = (distance*360/self.onerot)
        self.set_local_origin(0, 0, track_angle)

        while True:
            self.locate(local=True)
            self.speed_calculator(motor_angle, speed, terminal_speed, g_cons, corector_cons*direction)
            self.motor_driver(self.L_speed, self.R_speed)

            if task:
                task()
            if self.extra_task:
                self.extra_task()

            #motor breaker
            if abs(self.local_x) > abs(distance) or self.interupt: 
                self.motor_braker(stop)
                break

    def align_wall_a(self, speed, task: object = None):
        """
         ### probably not finished
        Parameters:
            - speed: Number - deg/s (+ forward, - backward)
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        """
        self.set_local_origin(0,0,0)
        L_speed = speed

        while self.acceleration < 3000 + abs(speed) * 5 and not self.interupt:
            self.locate(local=True)
            self.get_acceleration()
            R_speed = motor_corector(self.local_Lw_angle, self.local_Rw_angle, speed)
            self.motor_driver(L_speed, R_speed)

            if task:
                task()
            if self.extra_task:
                self.extra_task()
        self.motor_braker(True)

    def align_wall_t(self, speed, time, task: object = None):
        """
        - nejsložitější jeď po nějakou dobu nějakou rychlostí.

        Parameters:
            - speed: Number - deg/s (+ forward, - backward)
            - time: Number - ms - how far the barrier is
            - taks: object - this is a looppart function that you would like to incorporate into this function (eg. print() -> print ; and it'll start printing empti lines every turn)
        """
        timer = StopWatch()
        StopWatch.reset(timer)
        self.set_local_origin(0,0,0)
        L_speed = speed

        while StopWatch.time(timer) <= time and not self.interupt:
            self.locate(local=True)
            R_speed = motor_corector(self.local_Lw_angle, self.local_Rw_angle, speed)
            self.motor_driver(L_speed, R_speed)
            
            if task:
                task()
            if self.extra_task:
                self.extra_task()
        self.motor_braker(True)

    #composite complex functions
    def ultralocate(self, ul: Ultrasonic, x: float, y: float):
        """
        being designed!
        """
        return None

    def setup(self, robot_speed: int, arm_speeds: list):
        timer = StopWatch()
        StopWatch.reset(timer)
        self.Lw.reset_angle()
        self.Rw.reset_angle()
        L_speed = robot_speed
        arm_time = 400
        aling_time = 500
        arm_done = []
        done = False
        for i in range(len(self.arms)):
            arm_speeds[i] = absclamp(arm_speeds[i], 1000, 100) 
            self.arms[i].stress = clamp(abs(self.arms[i].stress), 8, 0.25)
            self.arms[i].run(arm_speeds[i])
            arm_done.append(False)

        while True:
            time = timer.time()
            R_speed = motor_corector(self.Lw.angle(), self.Rw.angle(), robot_speed)
            self.motor_driver(L_speed, R_speed)

            if time > arm_time:
                for i in range(len(self.arms)):
                    cons = abs(clamp(800/arm_speeds[i], 6, 1.5))*self.arms[i].stress
                    #cons(constant) = how many times the motor speed has to decrease to stop the motor.
                    arm_speed = abs(self.arms[i].speed())
                    if arm_speed < abs(arm_speeds[i]/cons):
                        self.arms[i].stop()
                        arm_done[i] = True
                arms_done = True
                for a_done in arm_done:
                    if a_done == False:
                        arms_done = False
            
            if time > aling_time:
                self.motor_braker(True)
                done = True

            if done and arms_done:
                break
        self.Lw.reset_angle(0)
        self.Rw.reset_angle(0)
        for arm in self.arms:
            arm.reset_angle(0)

    #neverending functions
    def gandalf(self):
        while True:
            self.hub.speaker.play_notes(["A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/4", "A3/8", "A3/16", "A3/16", "A3/4", "R/8", "C4/4", "A3/8", "R/8", "G3/8", "G3/8", "F3/8", "R/8", "D3/8", "D3/8", "E3/8", "F3/8", "D3/8"], 130)

class Mission:
    def __init__(self, robot: Robot, x: float, y: float, orientation: float, arm_setup: list, setup_speed: int = 1000):
        self.robot = robot
        self.x = x
        self.y = y
        self.orientation = orientation
        self.arm_setup = arm_setup
        self.setup_speed = setup_speed
        self.body = []
        self.done = False

    def add_body(self, *command: object):
        self.body = command

    def start(self):
        if self.done:
            for i in range(len(self.robot.arms)):
                arm = self.robot.arms[i]
                setup = self.arm_setup[i]
                arm.run_target(self.setup_speed, setup, wait=False)
            self.robot.straight_position(self.x, self.y, 1) ###
            self.robot.turn(self.orientation, 0)
            for command in self.body:
                command()
