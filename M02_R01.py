from M01_Inicialization import*
#def missions

#preparation
m10 = Setup(bot, 140, 113, 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

#mission 1 clear the area
m11 = Mission(bot, 475, 595, 60, [85, 300])
def m11_body():
    La.target(225)
    bot.straight_position(300, 520, -1)
    bot.straight_position(400, 860, 1)
m11.add_body(m11_body)

#mission 2 coral
m12 = Mission(bot, 430, 800, 180, [105, 760])
def m12_body():
    bot.straight_g(75, 50, True, 180)
    La.target(100)
    La.target(95, wait=False)
    bot.straight_g(50)
    bot.straight_g(-20)
    La.target(140)
    bot.straight_g(20)
    bot.straight_g(20)
    Ra.target(1000)
    bot.straight_g(-100)
m12.add_body(m12_body)

#mission 3 shark
m13 = Mission(bot, 320, -220, 135, [100, 1300])
def m13_body():
    bot.straight_g(30, 70, True, 135)
    La.target(20)
    bot.straight_g(-150)
m13.add_body(m13_body)

#mission 4 reef
m14 = Mission(bot, 360, 960, 25, [160, 1300])
def m14_body():
    bot.straight_g(35)
    La.target(90)
    bot.straight_g(-102)
    bot.turn(70, 0, 500, speed=300)
    Ra.target(900, wait=False)
    bot.straight_position(470, 790, -1)
    bot.turn(90, 0)
    Ra.target(1200)
    bot.straight_g(50)
    Ra.target(600)
    bot.straight_g(-60)
m14.add_body(m14_body)

#mission 5 bojka sample
m15 = Mission(bot, 840, 845, 30, [160, 1300])
def m15_body():
    Ra.target(100, wait=False)
    bot.turn(90, 0)
    bot.straight_g(50)
    Ra.target(1300)
    bot.straight_g(-60)
m15.add_body(m15_body)

#mission 6 loď
m16 = Mission(bot, -400, 835, -45, [10, 1300])
def m16_body():
    bot.straight_g(165, 50, True, -45)
    La.target(130)#####################dodělat
    bot.straight_g(70)
    bot.straight_g(-200)
m16.add_body(m16_body)

#mission 7 chaluha na špízu
m17 = Mission(bot, 0, 0, 5, [45, 1300])
def m17_body():
    return None

#def ride
r1 = Ride(Color.GREEN, m10, m11, m12, m13, m14, m15, m16)

#MM micro managrer
if __name__ == "Main":
    r1.start()