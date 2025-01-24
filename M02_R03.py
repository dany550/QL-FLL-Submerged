from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -200, [-500, -200])

m31 = Mission(bot, 885, 380, 135, [100, 0])
def m21_body():
    bot.straight_g(120)
    Ra.target(90)
    bot.straight_g(-120)
m31.add_body(m21_body)

#m32 = Mission()
def m22_body():
    None
#m32.add_body(m22_body)

r3 = Ride(Color.GREEN, m30, m31)

#MM micro managrer
if __name__ == "Main":
    r3.start()