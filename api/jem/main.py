#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
from jem_help import jem_help
from jemled import *
from jembuzzer import *
from jemrange import *

global wlan
wlan = setup_wifi()

#from kits.kit import Kit

#kit = Kit()
#kit.start()
RED = 0x880000 # red, green blue
GREEN = 0x008800
BLUE = 0x000088
jem_led = JemLed()
jem_buzz = JemBuzzer()
jem_range = JemRange()

def color(c = RED):
    jem_led.set_color(c)

def buzz(freq=100):
    if freq == 0:
        jem_buzz.stop()
    else:
        jem_buzz.start(freq)

def distance():
    print("%s" % jem_range.distance)
