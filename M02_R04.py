from M01_Inicialization import*
#def missions

m40 = Setup(bot, 2000 -120 , 110, 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

m41 = Mission(bot, -50, 340, 90, [180,0])
def m41_body():
    bot.straight_g(80, speed=100)
    bot.straight_g(-120)
m41.add_body(m41_body)

m42 = Mission(bot,-395, 500, 135, [0, 0])
def m42_body():
    bot.straight_g(100)
    bot.straight_g(-100)
m42.add_body(m42_body)

m43 = Mission(bot, -330, -280, 45, [0, 100])
def m43_body():
    bot.straight_g(180, speed = 500)
    bot.straight_g(-150)
m43.add_body(m43_body)
m43.add_checkpoint(-400, 800, 1)

m44 = Mission(bot, -625, -280, 90, [180, 300], -1)
def m44_body():
    bot.straight_g(60, 50, True, 90)
    Ra.target(600)
m44.add_body(m44_body)

m45 = Mission(bot, -880, 850, 135, [180, 100], -1)
def m45_body():
    bot.straight_g(80)
    Ra.target(650)
m45.add_body(m45_body)
m45.add_checkpoint(-820, 840, 1)

m46 = Mission(bot, -800, 800, 135, [180, 500], -1)


r4 = Ride(Color.YELLOW, m40, m41, m42, m43, m44, m45, m46)

#MM micro managrer
if __name__ == "Main":
    r4.start()