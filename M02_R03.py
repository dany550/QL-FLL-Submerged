from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [-500, -200])

m31 = Mission(bot, 855, 360, 135, [100, 0])
def m21_body():
    bot.straight_position(780, 450, 1)
    bot.turn(135, 0)
    #bot.straight_g(130)
    Ra.target(200, 200)
    Ra.target(10)
    bot.straight_g(-100)
m31.add_body(m21_body)

m32 = Mission(bot, -710, 390, 135, [100, 0], -1)
def m22_body():
    bot.straight_position(-200, 200, -1)
m32.add_body(m22_body)

r3 = Ride(Color.GREEN, m30, m31, m32)

#MM micro managrer
if __name__ == "Main":
    r3.start()