from M01_Inicialization import*
#def missions

m40 = Setup(bot, 2000 - 120 , 110, 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

#useless
m41 = Mission(bot, -50, 340, 90, [65,0])
def m41_body():
    bot.straight_g(80, speed=100)
    bot.straight_g(-200)
m41.add_body(m41_body)

m42 = Mission(bot,-395, 500, 135, [20, 600])
def m42_body():
    bot.straight_g(120)
    bot.straight_g(-100)
   # bot.straight_position(-350, 800, 1)
    
m42.add_body(m42_body)

m43 = Mission(bot, -500, 900, 115, [150, 600])
def m43_body():
    Ra.target(160)
    bot.straight_g(-100, 50, True, 100)
    bot.straight_g(110, 50, True, 129)
    Ra.target(650)
    bot.straight_g(-100)
m43.add_body(m43_body)
m43.add_checkpoint(-400, 800, 1)

m44 = Mission(bot, -335, 875, 10, [180, 400])
def m44_body():
    Ra.target(10)
    bot.straight_g(-150, 900)
    Ra.target(600,1000,False)
    bot.straight_g(-100)
m44.add_body(m44_body)

m45 = Mission(bot, 1120, -270, 135, [180, 0], -1)
def m45_body():
    bot.straight_g(80)
    Ra.target(660)
m45.add_body(m45_body)
m45.add_checkpoint(-820, 840, 1)

m46 = Mission(bot, -820, 840, 135, [180, 500], -1)


r4 = Ride(Color.YELLOW, m40, m42, m43, m44 , m45, m46)

#MM micro managrer
if __name__ == "Main":
    r4.start()