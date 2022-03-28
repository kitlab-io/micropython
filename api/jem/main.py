#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
import pycom

global wlan
wlan = setup_wifi()

from kits import kit_main
kit = None

if kit_main.kit_available:
    kit = kit_main.load_kit(rc=rc, kit='demo')
"""
import time
from kits.lantern.matrix_demo import MatrixDemo
d = MatrixDemo()
time.sleep(1)
"""
