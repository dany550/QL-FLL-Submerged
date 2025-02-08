from M01_Inicialization import*
#def missions

m20 = Setup(bot, 2000 - 120, 110 , 90, [[0,0],[2000, 1140]], -50, [1000, -1000])


m21 = Mission(bot, 250, 580, 185, [0, 0])
def m21_body(): 
    bot.straight_g(-170)
    bot.straight_g(100)
m21.add_body(m21_body)
m21.add_checkpoint(-800, 410, 1)

m22 = Mission(bot, 10, 200, 45, [0,0], -1)

r2 = Ride(Color.BLUE, m20, m21, m22)

#MM micro managrer
if __name__ == "Main":
    r2.start()