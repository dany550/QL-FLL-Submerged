from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [-500, -200])

m31 = Mission(bot, 770, 440, 45, [180, 100])
def m31_body():
    Ra.target(460, 500)
    #prvni hodnota mozna jinak
    bot.straight_g(-70, 500)
    Ra.target(550, 1000 , False)
    bot.straight_g(-40)
m31.add_body(m31_body)
m31.add_checkpoint(950,380,1)

m32 = Mission(bot, -310, 350, 160, [180, 0], -1, turn=False, terminal_speed=500)
def m32_body():
    bot.straight_position(-250, 200, -1)
    #cela mozna jinak
    bot.straight_position(-150, 150, -1)
m32.add_body(m32_body)
m32.add_checkpoint(-1,350,1)

r3 = Ride(Color.GREEN, m30, m31, m32)

#MM micro managrer
if __name__ == "Main":
    r3.start()