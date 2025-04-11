from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [0, -200])

m31 = Mission(bot, 320, 680, 0, [10, 0])
def m31_body():
    bot.straight_g(170, speed=150)
    bot.straight_g(-150)
m31.add_body(m31_body)

m32 = Mission(bot, 440, 220, 0,[250,10],-1)
def m32_body():
    Ra.target(800)
m32.add_body(m32_body)

m321 = Mission(bot, 240, 190, 0,[250,10],-1)
def m321_body():
    Ra.target(750)
    bot.straight_g(260, 300, set_angle=True, angle=11)
    bot.straight_g(110,300,set_angle=True,angle=-5)
    bot.straight_g(450, set_angle=True, angle=-15)
    Ra.target(10)
    bot.straight_g(-150)

m321.add_body(m321_body)

m33 = Mission(bot, 960, 325, 45,[250,10])
def m33_body():
    La.target(-100)
    bot.straight_g(180, 300, set_angle=True, angle=45)
    bot.straight_g(800,set_angle=True, angle=-15)

m33.add_body(m33_body)



r3 = Ride(Color.GREEN, m30, m31, m32, m33)

#MM micro managrer
if __name__ == "Main":
    r3.start()