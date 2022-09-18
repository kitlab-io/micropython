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

    for i in range(10):
        led.set_color(red) # set color to red
        time.sleep(0.5) # wait 1/2 second
        led.off() # turn off the led
        time.sleep(0.5) # wait 1/2 second
