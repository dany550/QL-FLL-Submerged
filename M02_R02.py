from M01_Inicialization import*
#def missions

m20 = Setup(bot, 2000 - 120, 110 , 90, [[0,0],[2000, 1140]], -50, [1000, -500])


m21 = Mission(bot, -615, 380, 180, [0, 400])
def m21_body(): 
    bot.straight_g(350)
    bot.straight_position(-800, 335, -1)
    #bot.straight_g(-150, 50, True, 150)
    bot.straight_g(250, 50, True, 180)
m21.add_body(m21_body)
m21.add_checkpoint(615, 400, 1)

m211 = Mission(bot, -830, 430, 180, [0, 500])
def m211_body():
    bot.straight_g(500, 50, True, 200)
m211.add_body(m211_body)

m22 = Mission(bot, 280, 630, 180, [0, 500], 1)
def m22_body():
    Ra.target(850, 500)
    bot.straight_g(-230, 50, True, 180, speed=400)
    bot.straight_g(100)
    bot.straight_g(-170, 50, True, 45)
    Ra.target(500, 500, False)
    bot.straight_g(-300)
m22.add_body(m22_body)

m23 = Mission(bot, 350, 105, 0, [0, 500])
def m23_body():
    Ra.target(100, 500)
    bot.straight_g(100)
    bot.straight_g(-50, 500, True, -10)
    Ra.target(200, wait=False)
    bot.straight_g(-500)
m23.add_body(m23_body)
r2 = Ride(Color.BLUE, m20, m211, m22)

#MM micro managrer
if __name__ == "Main":
    r2.start()