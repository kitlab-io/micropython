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
    print("loading a kit")
    kit = kit_main.load_kit(rc=rc, kit='window')
else:
    print("no kit selected")
