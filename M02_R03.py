from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [-500, -200])

m31 = Mission(bot, 320, 685, 0, [10, 0])
def m31_body():
    bot.straight_g(170, speed=200)
    bot.straight_g(-150)
    bot.straight_position(500, 370, 1)
m31.add_body(m31_body)

m32 = Mission(bot, -310, 350, 160, [180, 0], -1, turn=False, terminal_speed=500)
def m32_body():
    bot.straight_position(-250, 200, -1, terminal_speed=900)
    #cela mozna jinak
    bot.straight_position(-170, 170, -1)
m32.add_body(m32_body)
m32.add_checkpoint(-1,350,1)

r3 = Ride(Color.GREEN, m30, m31)

#MM micro managrer
if __name__ == "Main":
    r3.start()