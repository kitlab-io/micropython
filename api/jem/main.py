#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
from jem_help import jem_help

global wlan
wlan = setup_wifi()

from kits.kit import Kit

kit = Kit()
kit.start()
