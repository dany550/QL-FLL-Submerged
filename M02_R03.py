from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [-500, -200])

m31 = Mission(bot, 930, 335, 140, [100, 0])
def m31_body():
    bot.straight_g(185)
    Ra.target(205, 400)
    Ra.target(10, 400)
    bot.straight_g(-100)
m31.add_body(m31_body)

m32 = Mission(bot, -710, 370, 160, [100, 0], -1)
def m32_body():
    bot.straight_position(-50, 100, -1)
m32.add_body(m32_body)

r3 = Ride(Color.GREEN, m30, m31, m32)

#MM micro managrer
if __name__ == "Main":
    r3.start()