# demo.py
# run some example code to demonstrate JEM features
from drivers.neopixel import Neopixel
from jem.jemimu import JemIMU
import _thread
import time

WINDOW_PIXEL_COUNT = 8*8 # 64 pixels
# Window Kit
class Window:
    def __init__(self, neopixel_leds=WINDOW_PIXEL_COUNT, rc_ble_service=None):
        self.neopixel = Neopixel(num_leds=neopixel_leds)
        self._run = False
        self._rc_ble_service = rc_ble_service
        self.imu = JemIMU()

    def start(self):
        self.start_main_thread()

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
        roll = self.imu.orientation['roll']
        while self._run:
            self.leveler(prev_roll, roll)
            prev_roll = roll
            roll = self.imu.orientation['roll']
            time.sleep(0.01)

    def _sparkle_with_motion(self, rainbow=False, count=10):
        # don't call this directly!
        # use the start_sparkle_motion_thread
        diff_roll = 0.0
        prev_roll = self.imu.orientation['roll']
        while self._run:
            if diff_roll >= 0.5:
                self.neopixel.sparkle(count=count, random_color=rainbow)
            time.sleep(0.01)

            new_roll = self.imu.orientation['roll']
            diff_roll = abs(new_roll - prev_roll)
            prev_roll = new_roll

    def start_sparkle_motion_thread(self, rainbow=True, count=100):
        self._run = True
        _thread.start_new_thread(self._sparkle_with_motion, (rainbow, count))

    def start_leveler_motion_thread(self, rainbow=True, count=100):
        self._run = True
        _thread.start_new_thread(self._leveler_with_motion, ())

    def stop_sparkle_motion_thread(self):
        self._run = False

    def stop_leveler_motion_thread(self):
        self._run = False

    def _main_thread(self):
        # put stuff that you want to run in the background here
        print("Window Kit main thread started")
        if not self._rc_ble_service:
            print("_main_thread failed: _rc_ble_service not set")
            return
        try:
            prev_roll = None
            while self._main_run:
                time.sleep(0.1)
                if not self._rc_ble_service.is_connected():
                    continue
                roll = self.imu.orientation['roll']
                if prev_roll != roll:
                    s = b"roll = %s" % roll
                    self._rc_ble_service.write_aux(s)
                    prev_roll = roll
        except Exception as e:
            print("_main_thread failed: %s" % e)
        print("Window Kit main thread stopped")

    def start_main_thread(self):
        print("start_main_thread")
        self._main_run = True
        _thread.start_new_thread(self._main_thread, ())
