#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *

wifi = setup_wifi()
from kits.demo.neopixel import Neopixel
pix = Neopixel()
