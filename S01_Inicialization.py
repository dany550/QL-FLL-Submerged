from tools import*

hub = PrimeHub()
Lw = Motor(Port.F, Direction.COUNTERCLOCKWISE)
Rw = Motor(Port.B)
Cs = ColorSensor(Port.E)
bot = Robot(hub, 27.9, 158, Lw, Rw)
Ra = Arm(Port.A, bot)
bot.extra_task = bot.interupter
bot.add_arms(Ra)
bot.hub.system.set_stop_button(Button.BLUETOOTH)