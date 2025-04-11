from M01_Inicialization import*
#def missions

m20 = Setup(bot, 2000 - 120, 110 , 90, [[0,0],[2000, 1140]], -50, [-1000, -500])

m21 = Mission(bot, -615, 370, 180, [10, 300])
def m21_body(): 
    bot.straight_g(30, 500)
    Ra.target(700, 1000, False)
    bot.straight_g(350)
    Ra.target(200, 1000)
    
m21.add_body(m21_body)
m21.add_checkpoint(-750, 410, 1) #set this to -750; 430 and wach the beauty

m22 = Mission(bot, 850, 405, 90, [10, 400], 1)
def m22_body():
    Ra.target(250)
    bot.straight_g(-100)
m22.add_body(m22_body)
m22.add_checkpoint(600, 420, 1)

m23 = Mission(bot, 20, 390, 90, [20, 150])
def m23_body():
    Ra.target(200)
    Ra.target(385, 200, False)
    bot.straight_g(180)
    Ra.target(300)
    bot.straight_g(-100, 900)
    bot.straight_position(150, 150, -1)
m23.add_body(m23_body)

m231 = Mission(bot, 340, 580, 180, [20, 10])
def m231_body():
    bot.straight_g(100)
    Ra.target(500)
    bot.straight_position(150, 150, -1)
m231.add_body(m231_body)
r2 = Ride(Color.BLUE, m20, m21, m22, m23)

#MM micro managrer
if __name__ == "Main":
    r2.start()