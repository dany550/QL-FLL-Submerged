from tools import *

hub = PrimeHub()
Lw = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
La = Arm(Port.C, gears=[20, 28])
Ra = Arm(Port.D)
bot = Robot(hub, 27.9, 158, Lw, Rw)

#preparation
bot.set_origin(140, 110, 90, [[0,0],[2000, 1140]])
bot.align_wall_t(-100, 500)
bot.set_origin(145, 110, 90, [[0,0],[2000, 1140]])
La.align(-500)
La.reset_angle(0)
Ra.align(-500)
Ra.reset_angle(0)
La.run_target(500, 50)
bot.straight_g(50, 900)

#bot.straight_position(x, y, kdyz dopredu tak 1 dozadu je -1)
#kdyz chces jet na souradnice ^
#bot.straight_g(vzdalenost, rychlost, True pokud chces pocatecni smer, pocatecni smer)
#kdyz chces jet jen rovne a dozadu ^
#La.run_target(rychlost 1000 max, pozice motoru 0 dole 225 nahorem, wait = false pokud chces prehravat naraz s dalsim radkem jinak nic sem nepis)
#zubata ruka ^
#Ra.run_angle(rychlost 1000 max, pozice motoru 100 je dole a 1300 nahore, wait = false pokud chces prehravat naraz s dalsim radkem jinak nic sem nepis)
#hak se snekem ^
#bot.turn(absolutni uhel, 0)
#toceni robota na miste ^
#absolutni uhel = 90° je vzdy ve smeru osy Y a 0° je vzdy ve smeru osy X

#mission 1 clear the area
La.run_target(1000, 85, wait=False)
bot.straight_position(475, 595, 1)

#bot.turn(60, 0)
La.run_target(1000, 225)
bot.straight_position(300, 520, -1)
bot.straight_position(400, 860, 1)

#mission 2 coral
Ra.run_target(1000, 760, wait=False)
La.run_target(1000, 105, wait=False)
bot.straight_position(430, 800, -1)

bot.straight_g(75, 50, True, 180)
La.run_target(1000, 100)
La.run_target(1000, 95, wait=False)
bot.straight_g(50)
bot.straight_g(-20)
La.run_target(1000, 140) ####
bot.straight_g(20)
bot.straight_g(20)
Ra.run_angle(1000, 500)
bot.straight_g(-100)

#mission 3 shark
La.run_target(1000, 100, wait=False)
Ra.run_target(1000, 1300, wait=False)
bot.straight_position(320, -220, 1)
bot.straight_g(30, 70, True, 135)
La.run_target(1000, 20)
bot.straight_g(-150)

#mission 4 reef
La.run_target(1000, 160, wait=False)
Ra.run_target(1000, 1300, wait=False)
bot.straight_position(360, 960, 1)
bot.turn(25, 0)
bot.straight_g(35)
La.run_target(1000, 90)
bot.straight_g(-102)
bot.turn(70, 0, 500, speed=300)
Ra.run_target(500, 900, wait=False)
bot.straight_position(470, 790, -1)
bot.turn(90, 0)
Ra.run_target(480, 1200)
bot.straight_g(50)
Ra.run_target(500, 600)
bot.straight_g(-60)

#mission 5 bojka sample
Ra.run_target(1000, 1300, wait=False)
bot.straight_g(50)
bot.turn(30, 0)
bot.straight_position(840, 845,1)
Ra.run_target(1000, 100, wait=False)
bot.turn(90, 0)
bot.straight_g(50)
Ra.run_target(1000, 1300)
bot.straight_g(-60)

#mission 6 loď
La.run_target(1000, 10)
bot.turn(0, 0, terminal_speed=400)
bot.straight_position(-400, 835, 1)
bot.straight_g(165, 50, True, -45)
La.run_target(1000, 130)#####################dodělat
bot.straight_g(70)
bot.straight_g(-200)

#mission 7 chaluha na špízu
#La.run_target(1000, 45)
#bot.turn(5, 0)
#bot.straight_position()