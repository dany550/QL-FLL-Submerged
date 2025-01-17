from M01_Inicialization import*
#def missions

#preparation
Ra.stress = 2
m10 = Setup(bot, 140, 113, 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

#mission 1 clear the area
m11 = Mission(bot, 470, 580, 50, [65, 300])
def m11_body():
    La.target(200)
    bot.straight_position(300, 520, -1)
    bot.straight_position(400, 860, 1)
m11.add_body(m11_body)
m11.add_checkpoint(430, 800, 1)

#mission 2 coral
m12 = Mission(bot, 430, 800, 180, [90, 760], -1)
def m12_body():
    bot.straight_g(75, 50, True, 180)
    La.target(85)
    La.target(80, wait=False)
    bot.straight_g(50)
    La.target(120)
    bot.straight_g(10)
    Ra.target(1200)
    bot.straight_g(-120)
m12.add_body(m12_body)

#mission 3 shark
m13 = Mission(bot, 320, -240, 135, [100, 1300])
def m13_body():
    bot.straight_g(30, 70, True, 135)
    La.target(20)
    bot.straight_g(-150)
m13.add_body(m13_body)

#mission 4 reef, potapec   dotyka se toho, zmen to, dikec
m14 = Mission(bot, 300, 930, 25, [160, 1300])
def m14_body():
    bot.straight_g(100)
    La.target(70)
    bot.straight_g(-102)
    bot.turn(70, 0, 500, speed=300)
    Ra.target(900, wait=False)
    La.target(80)
    bot.straight_position(465, 770, -1)
    bot.turn(90, 0)
    Ra.target(1200)
    bot.straight_g(50)
    Ra.target(600)
    bot.straight_g(-40)
    Ra.target(1200)
    bot.straight_position(550, 850, 1)
m14.add_body(m14_body)
m14.add_checkpoint(550, 820, 1)

#mission 5 bojka sample
m15 = Mission(bot, 840, 825, 30, [160, 1300])
def m15_body():
    Ra.target(100, wait=False)
    bot.turn(90, 0)
    bot.straight_g(55)
    Ra.target(1300)
    bot.straight_g(-65)
m15.add_body(m15_body)
#m15.add_checkpoint(840, 815, 1)

#mission 6 lod
m16 = Mission(bot, -390, 820, -45, [-5, 1300])
def m16_body():
    #print(1/0)
    bot.straight_g(145, 50, True, -45)
    La.target(130,300,wait = False)
    bot.straight_g(70,20)
    La.target(200,wait = False)
    bot.straight_g(30)
    bot.straight_g(-200)
m16.add_body(m16_body)

#mission 7 chaluha na špízu
m17 = Mission(bot, -300, 760, 45, [80, 1300])
def m17_body():
    bot.straight_g(180)
    bot.straight_g(-180)
    bot.turn(0,0)
    La.target(10,wait=False)
    bot.straight_g(75)
    #bot.straight_position(-230, 770, 1)
    La.target(60)
    bot.straight_g(-75)

    return None
m17.add_body(m17_body)

m18 = Mission(bot, -300, 770, -80, [60, 1300], direction=-1)
def m18_body():
    bot.straight_position(-400, 550, 1)
    bot.straight_position(-100, 150, 1)
    return None
m18.add_body(m18_body)

#def ride
r1 = Ride(Color.RED, m10, m11, m12, m13, m14, m15, m16, m17,m18)

#MM micro managrer
if __name__ == "Main":
    r1.start()