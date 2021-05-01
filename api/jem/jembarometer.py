"""jembarometer.py
Desc: hardware abstraction layer around pressure sensor that includes temperature and humidity measurements
Driver used: bme280
Example:
    >> bar = JemBarometer()
    >> data = bar.read()
    >> bar.power_down() # if available, will put device to sleep to save power
    >> bar.pn # part number of driver
    >> "bme280"
"""

from drivers.bme280 import BME280

class JemBarometer(BME280):
    def __init__(self, i2c=None):
        """Initialize JemDevice parent class and then set the comm and bme280 driver objects"""
        super(JemBarometer, self).__init__(i2c=i2c, address=BME280.I2C_ADDRESS)

    def read(self):
        try:
            t, p, h, a = self.data
            return {'temp':t, 'pressure':p, 'humidity': h, 'altitude': a}
        except Exception as e:
            print("read failed - from {0} device - {1}".format(self.pn, e))
