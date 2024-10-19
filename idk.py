from inicialization import*
from tools import*

from mathClasses import*

class Bot:
    def __init__(self):
        self.pos = Vec(0,0)
    def SetPos(self, pos):
        self.pos = pos


defHeading = Vec(1,0) # jak byl robot na začátku namířen
rotConstant = 0.5 # ovlivňuje jak mo robot zatáčí když se chce držet dráhy

def straight_position(startPos: Vec, endPos: Vec, speed: float = 50):
    """
    supr cupr metoda
    """
    moveVec = endPos - startPos
    if moveVec.length == 0:
        return
    
    botPos = startPos
    angleBetween =  atan2(moveVec.x,moveVec.y)
    # úhel mezi startPos a osou x (resp. vec[1,0]) 
    rotMat = Matrix.rot(-angleBetween)

    # TODO otoc robota spravnym smerem
    turn(degrees(angleBetween), 0)
    
    lastAngleL = Lw.angle()
    lastAngleR = Rw.angle()
    lastAngle = hub.imu.heading()
    while True:    
        deltaAngleL = Lw.angle() - lastAngleL # delty hodnot
        deltaAngleR = Rw.angle() - lastAngleR
        deltaAngle = hub.imu.heading() - lastAngle
        lastAngleL = Lw.angle()
        lastAngleR = Rw.angle()
        lastAngle = hub.imu.heading()
        
        # posun pozice robota
        if deltaAngleL == deltaAngleR: # pokud jel pouze rovně
            botPos += deltaAngleR * wheelRadius * (defHeading*Matrix.rot(-radians(hub.imu.heading())))
        elif deltaAngleL > deltaAngleR: # pokud zatáčel doprava
            r = deltaAngleR*axle/(deltaAngleL-deltaAngleR) + axle*0.5 # poloměr kružnice kterou střed robota opisoval
            center = Matrix.rot(-radians(deltaAngle)) * (-r * Vec.yAxis) # střed -||-
            circleAngle = (deltaAngleR * wheelRadius)/((r-axle*0.5)*2*pi) # jakou část (v radiánech) kružnice robot opsal
            botPos += Matrix.rot(circleAngle) * (-center) + center # posunutí aktuální pozice po kružnici
        else: # pokud zatáčel doleva
            r = deltaAngleL*axle/(deltaAngleR-deltaAngleL) + axle*0.5
            center = Matrix.rot(-radians(deltaAngle)) * (r * Vec.yAxis)
            circleAngle = (deltaAngleL * wheelRadius)/((r-axle*0.5)*2*pi)
            botPos += Matrix.rot(circleAngle) * (-center) + center
        
        transformedPos = rotMat * (botPos - startPos)
        y = transformedPos.y * rotConstant # určuje jestli je robot pod/nad svou dráhou
        R_speed = speed
        L_speed = speed
        if y > 0:
            R_speed = 1/(abs(y)+1) * speed #zpomalí motor podle funkce zavíslé na y
        elif y < 0:
            L_speed = 1/(abs(y)+1) * speed

        motor_driver(L_speed, R_speed, True, True)

        # motor breaker
        if transformedPos.x >= moveVec.lenght:
            motor_driver(L_speed, R_speed, False, False)
            break
 
        wait(10)
