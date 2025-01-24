from M01_Inicialization import*
#def missions

m20 = Setup(bot, 2000 - 120, 110 , 90, [[0,0],[2000, 1140]], -200, [-500, -1000])

m21 = Mission(bot, -450, 280, 180, [0, 0])
def m21_body():
    bot.straight_g(50)
    Ra.target(720, 1000, True)
    bot.straight_g(200)
    bot.straight_g(-100)
m21.add_body(m21_body)

m22 = Mission(bot, 1000, 300, 180, [0, 0])
def m22_body():
    None
m22.add_body(m22_body)

r2 = Ride(Color.BLUE, m20, m21, m22)

#MM micro managrer
if __name__ == "Main":
    r2.start()