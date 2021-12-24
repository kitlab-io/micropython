#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
global wlan
wlan = setup_wifi()
from kits.demo.demo import Demo

#demo = Demo() # run demo to use neopixels for example
