#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
global wlan
wlan = setup_wifi()

import time
from kits.demo.matrix_demo import MatrixDemo
d = MatrixDemo()
time.sleep(1)

"""
from kits.demo.demo import Demo
demo = Demo() # run demo to use neopixels for example
demo.start_sparkle_motion_thread()
"""
