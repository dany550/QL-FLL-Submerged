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

m211 = Mission(bot, -615, 380, 180, [0, 500])
def m211_body():
    bot.straight_g(500, 900, True, 185)
m211.add_body(m211_body)

m22 = Mission(bot, 240 ,545, 180, [0, 500], 1)
def m22_body():
    Ra.target(850, 500)
    bot.straight_g(-250, 50, True, 180, speed=300)
    bot.straight_g(150)
    bot.straight_g(-150, 50, True, 45)
    Ra.target(500, 500, False)
m22.add_body(m22_body)

m23 = Mission(bot, 350, 165, 0, [0, 500])
def m23_body():
    Ra.target(100, 500)
    bot.straight_g(50)
    bot.straight_g(-20, 900)
    Ra.target(100, wait=False)
    bot.straight_g(-450)
m23.add_body(m23_body)
r2 = Ride(Color.BLUE, m20, m211, m22, m23)

#MM micro managrer
if __name__ == "Main":
    r2.start()