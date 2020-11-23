"""jembarometer.py
Desc: hardware abstraction layer around pressure sensor that includes temperature and humidity measurements
Driver used: bme280
Example:
    >> bar = JemBarometer()
    >> data = bar.read()
    >>
    >> bar.power_down() # if available, will put device to sleep to save power
    >> bar.pn # part number of driver
    >> "bme280"
"""

from drivers.bme280 import BME280
from helpers.helpers import Struct


class JemBarometer(BME280):
    def __init__(self, i2c=None):
        """Initialize JemDevice parent class and then set the comm and bme280 driver objects"""
        super(JemBarometer, self).__init__(i2c=i2c, address=BME280.I2C_ADDRESS)

    def read(self):
        try:
            t, p, h, a = self.data
            bar_struct = Struct(temp=t, press=p, hum=h, alt=a)
            return bar_struct
        except Exception as e:
            print("Failed to get sensor data from {0} device - {1}".format(self.pn, e))
