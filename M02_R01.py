from M01_Inicialization import*
#def missions

#preparation
Ra.stress = 2
m10 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

#mission 1 clear the area
m11 = Mission(bot, 470, 575, 50, [65, 1000])
def m11_body():
    La.target(200)
    bot.straight_position(300, 520, -1)
    #bot.straight_position(400, 860, 1)
m11.add_body(m11_body)
#m11.add_checkpoint(430, 800, 1)

#mission 2 coral
m12 = Mission(bot, 430, 790, 180, [100, 300]) #90
def m12_body():
    Ra.target(830,wait=False)
    bot.straight_g(90, 50, True, 180)
    #La.target(90)
    La.target(80, speed = 1000)
    #wait(1000)
    bot.straight_g(50,speed = 600)
    #La.target(120)
    Ra.target(1200)
    bot.straight_g(-120)
m12.add_body(m12_body)

#mission 3 shark
m13 = Mission(bot, 320, -240, 135, [100, 1300])
def m13_body():
    bot.straight_g(40, 70, True, 135)
    La.target(20)
    #bot.straight_g(-100, 900)
m13.add_body(m13_body)

#mission 4 reef, potapec dotyka se toho, zmen to, dikec
m14 = Mission(bot, 300, 910, 20.5, [160, 1300])
def m14_body():
    bot.straight_g(90)
    La.target(70)
    bot.straight_g(-102)
    bot.turn(70, 0, 500, speed=300)
    Ra.target(900, wait=False)
    La.target(200)
    bot.straight_position(445, 770, -1)
    bot.turn(90, 0)
    Ra.target(1200)
    bot.straight_g(50)
    Ra.target(600)
    bot.straight_g(-40)
    Ra.target(1200)
    bot.straight_position(550, 850, 1)
m14.add_body(m14_body)
m14.add_checkpoint(550, 860, 1)

m141 = Mission(bot, 475, 770, 90, [160, 1200], -1)
def m141_body():
    bot.straight_g(50)
    Ra.target(800)
    bot.straight_g(-70)
    Ra.target(700, 1000, False)
    bot.straight_g(70, 900, True, 75)
    bot.straight_g(80, 50, True, 90)
    Ra.target(200)
    Ra.target(800)
    bot.straight_g(-60)
m141.add_body(m141_body)

#mission 5 bojka sample
m15 = Mission(bot, 805, 832, 30, [160, 1300])
def m15_body():
    Ra.target(100, wait=False)
    bot.turn(90, 0)
    bot.straight_g(60)
    Ra.target(1300)
    bot.turn(105, 0)
    bot.straight_g(-94, 50, True, 105)
m15.add_body(m15_body)
m15.add_checkpoint(1000, 800, 1)

#return
m16 = Mission(bot, -770, 450, -45,[100, 1300], terminal_speed=900, turn=False)
def m16_body():
    bot.straight_position(-260, 200, 1)
m16.add_body(m16_body)


#useless
m18 = Mission(bot, -400, 800, 0, [200, 1300], direction=1)
def m18_body():
    #bot.straight_position(-260, -270, 1)
    #bot.straight_position(-450, -350, -1)
    bot.straight_position(-150, 70, -1)
    La.target(10)
    return None
m18.add_body(m18_body)
m18.add_checkpoint(-150, 70, 1)

r1 = Ride(Color.RED, m10, m11, m12, m13, m141, m15, m16)

#MM micro managrer
if __name__ == "Main":
    r1.start()