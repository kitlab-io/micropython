# simple.py
from jem import jemrange, jemled

led = jemled.JemLed()
range = jemrange.JemRange()

# Tutorial_1

from jem.jembuzzer import JemBuzzer
import time

# create new buzzer based on smt0540s2r driver (see jem/drivers)
buzzer = JemBuzzer()

# define our new function
def buzz(freq_hz=100, time_sec=1):
    # global: you don't have to do this, but it's good practice
    # just let's python know that buzzer object was defined somewhere else
    global buzzer

    # make sound based on the frequency (Hertz) for some time
    buzzer.start(freq_hz)
    time.sleep(time_sec)
    buzzer.stop()

# Tutorial_1 !


running = True
def run():
    print("simple kit started")
