# jemled.py
# just a wrapper around pycom.rgbled
import pycom

class JemLed:
    RED = 0x880000 # red, green blue
    GREEN = 0x008800
    BLUE = 0x000088
    
    def __init__(self):
        self.color = JemLed.RED
        self.heartbeat_disabled = False

    def set_color(self, color):
        """ ex: red color = 0x880000 or JemLed.RED """
        self.color = color
        if not self.heartbeat_disabled:
            pycom.heartbeat(False)
            self.heartbeat_disabled = True
        pycom.rgbled(self.color)

    def off(self):
        pycom.rgbled(0x000000)

if __name__ == "__main__":
    import time
    led = JemLed()

    red = 0xFF0000
    print("turn on led")
    led.set_color(red) # set color to red
    print("sleep")
    time.sleep(3) # wait 3 seconds
    print("turn off led")
    led.off() # turn off the led
