# demo.py
# run some example code to demonstrate JEM features
from jem import Jem
from neopixel import Neopixel
import pycom
class Demo:
    def __init__(self):
        self.jem = Jem()
        self.neopixel = Neopixel()

    def toggle_led(color1=0x440000, color2=0x004400, duration=10.0):
        start = time.time()
        pycom.heartbeat(False)
        while (time.time() - start) < duration:
            pycom.rgbled(color1)
            time.sleep(1)
            pycom.rgbled(color2)
            time.sleep(1)
