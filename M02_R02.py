from M01_Inicialization import*
#def missions

m20 = Setup(bot, 2000 - 120, 110 , 90, [[0,0],[2000, 1140]], -50, [1000, -500])

m21 = Mission(bot, -615, 370, 180, [0, 300], setup_speed=500)
def m21_body(): 
    bot.straight_g(30, 500)
    Ra.target(600, 500, False)
    bot.straight_g(340)
    Ra.target(200, 500)
    #bot.straight_position(-800, 335, -1)
    #bot.straight_g(-150, 50, True, 150)
    bot.straight_g(350, 50, True, 180)
m21.add_body(m21_body)
m21.add_checkpoint(-750, 400, 1)
#m21.add_checkpoint(600, 400, 1)

#useless
m211 = Mission(bot, -830, 410, 180, [0, 500])
def m211_body():
    bot.straight_g(500, 50, True, 200)
m211.add_body(m211_body)

m22 = Mission(bot, 280, 640, 180, [0, 500], 0)
def m22_body():
    Ra.target(850, 500)
    
    bot.straight_g(-280, 100, True, 180, speed=400)
    bot.straight_g(100)
    bot.straight_g(170, 900, True, 225)
    #Ra.target(500, 500, False)
    bot.straight_g(400)
m22.add_body(m22_body)
m22.add_checkpoint(100,150,-1)

m23 = Mission(bot, 350, 120, 0, [0, 500])
def m23_body():
    Ra.target(100, 500)
    bot.straight_g(100)
    bot.straight_g(-50, 500, True, -10)
    Ra.target(200, wait=False)
    bot.straight_g(-500)
m23.add_body(m23_body)
r2 = Ride(Color.BLUE, m20, m21, m22)

#MM micro managrer
if __name__ == "Main":
    r2.start()