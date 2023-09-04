from network import WLAN
wlan = None

def setup_wifi(name="JemWifi"):
    global wlan
    wlan = WLAN()
    wlan.init(mode=WLAN.AP, ssid=name)
    print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface
    return wlan

if __name__ == "__main__":
    # NOTE: don't do this while connected to jem wifi or won't work as expected
    global wifi
    wifi = setup_wifi("ExampleWifi")
    # now you should see jem wifi as 'ExampleWifi'
