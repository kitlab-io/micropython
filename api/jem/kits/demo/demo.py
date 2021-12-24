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

    def leveler(self, prev_roll, roll):
        c=(127, 127, 127)
        max_pixels = self.neopixel.num_leds
        max_roll = 90.0
        first_pixel = int(max_pixels/2)
        last_pixel = int(first_pixel + roll * (max_pixels/2)/max_roll)
        prev_last_pixel = int(first_pixel + prev_roll * (max_pixels/2)/max_roll)
        dir = 1
        if last_pixel < prev_last_pixel:
            dir = -1
            c = (0,0,0)
        self.neopixel.set_pixels(start_pixel=prev_last_pixel, end_pixel=last_pixel, c=c, dir=dir)

    def _leveler_with_motion(self):
        prev_roll = 0
        roll = self.jem.imu.orientation['roll']
        while self._run:
            self.leveler(prev_roll, roll)
            prev_roll = roll
            roll = self.jem.imu.orientation['roll']
            time.sleep(0.01)


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

    def start_leveler_motion_thread(self, rainbow=True, count=10):
        self._run = True
        _thread.start_new_thread(self._leveler_with_motion, ())

    def stop_sparkle_motion_thread(self):
        self._run = False

    def stop_leveler_motion_thread(self):
        self._run = False

    def toggle_led(self, color1=0x440000, color2=0x004400, duration=10.0):
        start = time.time()
        pycom.heartbeat(False)
        while (time.time() - start) < duration:
            pycom.rgbled(color1)
            time.sleep(1)
            pycom.rgbled(color2)
            time.sleep(1)
