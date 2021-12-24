# demo.py
# run some example code to demonstrate JEM features
from jem import Jem
from kits.demo.neopixel import Neopixel
import pycom
import _thread
import time
# Demo
class Demo:
    def __init__(self, neopixel_leds=64):
        self.jem = Jem()
        self.neopixel = Neopixel(num_leds=neopixel_leds)
        self._run = False

    def _sparkle_with_motion(self, rainbow=False, count=10):
        # don't call this directly!
        # use the start_sparkle_motion_thread
        diff_roll = 0.0
        prev_roll = self.jem.imu.orientation['roll']
        while self._run:
            if diff_roll >= 0.5:
                self.neopixel.sparkle(count=count, random_color=rainbow)
            time.sleep(0.1)

            new_roll = self.jem.imu.orientation['roll']
            diff_roll = abs(new_roll - prev_roll)
            prev_roll = new_roll


    def start_sparkle_motion_thread(self, rainbow=True, count=10):
        self._run = True
        _thread.start_new_thread(self._sparkle_with_motion, (rainbow, count))

    def stop_sparkle_motion_thread(self):
        self._run = False


    def toggle_led(self, color1=0x440000, color2=0x004400, duration=10.0):
        start = time.time()
        pycom.heartbeat(False)
        while (time.time() - start) < duration:
            pycom.rgbled(color1)
            time.sleep(1)
            pycom.rgbled(color2)
            time.sleep(1)
