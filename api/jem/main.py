#main.py
from kits import kit_main
kit_main.load_kit()

from network import WLAN
def setup_wifi():
    wlan = WLAN()

    wlan.init(mode=WLAN.AP, ssid='TestJem')
    #use the line below to apply a password
    #wlan.init(ssid="hi", auth=(WLAN.WPA2, "eightletters"))
    print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface
    return wlan
