from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [-500, -200])

m311 = Mission(bot, 130, 460, 90, [10, 450])
def m311_body():
    Ra.target(100)
    #bot.straight_g (50)
m311.add_body(m311_body)

m31 = Mission(bot, 765, 450, 45, [180, 100])
def m31_body():
    Ra.target(400, 500)
    #prvni hodnota mozna jinak
    bot.straight_g(-70, 500)
    Ra.target(550, 1000 , False)
    bot.straight_g(-40)
m31.add_body(m31_body)
m31.add_checkpoint(950,380,1)

m32 = Mission(bot, -310, 350, 160, [180, 0], -1, turn=False, terminal_speed=500)
def m32_body():
    bot.straight_position(-250, 200, -1, terminal_speed=900)
    #cela mozna jinak
    bot.straight_position(-170, 170, -1)
m32.add_body(m32_body)
m32.add_checkpoint(-1,350,1)

r3 = Ride(Color.GREEN, m30, m311)

#MM micro managrer
if __name__ == "Main":
    r3.start()