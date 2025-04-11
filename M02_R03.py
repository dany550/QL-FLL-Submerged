from M01_Inicialization import*
#def missions

m30 = Setup(bot, 130, 113, 90, [[0,0],[2000, 1140]], -50, [0, -1000])

m31 = Mission(bot, 320, 685, 0, [10, 10])
def m31_body():
    bot.straight_g(180, speed=400)
    bot.straight_g(-130)
    #bot.straight_position(500, 370, 1)
m31.add_body(m31_body)

m32 = Mission(bot, 230, 170, 0, [0, 10], -1)
def m32_body():
    Ra.target(750)
    bot.straight_g(150, 300, set_angle=True, angle=10)
    bot.straight_g(300, set_angle=True, angle=0)
    Ra.target(10)
    bot.straight_g(70)
m32.add_body(m32_body)
m32.add_checkpoint(-1,350,1)

m33 = Mission(bot, 950, 340, 45, [0, 10], 1)
def m33_body():
    La.target(-70)
m33.add_body(m33_body)

m34 = Mission(bot, 1550, 340, 45, [0, 10], 1, turn=False, terminal_speed=500)
def m34_body():
    bot.straight_position(-150, 150, 1)
m34.add_body(m34_body)

r3 = Ride(Color.GREEN, m30, m31, m32, m33, m34)

#MM micro managrer
if __name__ == "Main":
    r3.start()