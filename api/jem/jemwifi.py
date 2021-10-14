from network import WLAN
wlan = None
def setup_wifi(name="JemWifi"):
    global wlan
    wlan = WLAN()
    wlan.init(mode=WLAN.AP, ssid=name)
    print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface
    return wlan
