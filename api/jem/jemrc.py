"""jemrc.py
Desc: hardware abstraction layer around GPIO expander that interfaces with the RC motor driver
Driver used: pcf8574
Example:
    >> bar = JemBarometer()
    >> data = bar.read()
    >> bar.power_down() # if available, will put device to sleep to save power
    >> bar.pn # part number of driver
    >> "bme280"
"""

from drivers.pcf8574 import PCF8574

class JemRC(PCF8574):
    def __init__(self, i2c=None):
        """Initialize JemDevice parent class and then init pcf8574 driver"""
        super(JemRC, self).__init__(i2c=i2c, address=PCF8574.I2C_ADDRESS)
