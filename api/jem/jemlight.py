"""jemlight.py
Desc: hardware abstraction layer around temt6000 light sensor.
Driver used: temt6000
Example:
    >> light = JemLight()
    >> light.analog
    >> 2030 # 0 - 4095
    >> light.voltage
    >> 1.8 # 0 - 3.3V
    >> light.intensity
    >> 45 # 0 - 100%
    >> light.power_down() # if available, will put device to sleep to save power
    >> light.pn # part number of driver
    >> "temt6000"
    >> light.interface # type of communication
    >> "i2c"
"""

from drivers.temt6000 import TEMT6000

class JemLight(TEMT6000):
    def __init__(self):
        """Initialize JemDevice parent class and then init temt6000 driver"""
        super(JemLight, self).__init__()
