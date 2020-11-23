"""jemrange.py
Desc: hardware abstraction layer around vl53l0x range sensor.
Driver used: vl53l0x
Example:
    >> range = JemRange()
    >> range.distance
    >> 56 # millimeters
    >> range.power_down() # if available, will put device to sleep to save power
    >> range.pn # part number of driver
    >> "vl53l0x"
"""

from drivers.vl53l0x import VL53L0X

class JemRange(VL53L0X):
    def __init__(self, i2c=None):
        """Initialize JemDevice parent class and then init vl53l0x driver"""
        super(JemRange, self).__init__(i2c=i2c, address=VL53L0X.I2C_ADDRESS, io_timeout_s=0)
