# demo.py
# run some example code to demonstrate JEM features
from jem import Jem
from kits.demo.neopixel import Neopixel
import pycom
# test
class Demo:
    def __init__(self, neopixel_leds=64):
        self.jem = Jem()
        self.neopixel = Neopixel(num_leds=neopixel_leds)

    def toggle_led(color1=0x440000, color2=0x004400, duration=10.0):
        start = time.time()
        pycom.heartbeat(False)
        while (time.time() - start) < duration:
            pycom.rgbled(color1)
            time.sleep(1)
            pycom.rgbled(color2)
            time.sleep(1)
