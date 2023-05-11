# jemled.py
# just a wrapper around pycom.rgbled
from machine import Pin
from neopixel import NeoPixel

# for single ws2812 led
class JemLed:
    RED = (0x88,0x00,0x00) # red, green blue
    GREEN = (0x00,0x88,0x00)
    BLUE = (0x00,0x00,0x88)

    def __init__(self):
        self.pin = Pin(0, Pin.OUT) # LED / BOOT PIN on JEM2 is GPIO0
        self.np = NeoPixel(self.pin, 1)   # create NeoPixel driver on GPIO0 for 1 pixel
        self.color = JemLed.RED

    def set_color(self, color):
        """ ex: red color = 0x880000 or JemLed.RED """
        self.color = color
        self.np[0] = color
        self.np.write()

    def off(self):
        pycom.rgbled(0x000000)

if __name__ == "__main__":
    import time
    led = JemLed()
    red = (0xFF, 0x00, 0x00)

    for i in range(10):
        led.set_color(red) # set color to red
        time.sleep(0.5) # wait 1/2 second
        led.off() # turn off the led
        time.sleep(0.5) # wait 1/2 second
