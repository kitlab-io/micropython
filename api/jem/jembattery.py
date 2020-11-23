"""jembattery.py
Desc: hardware abstraction layer around bq27441 fuel gauge ic connected to Lipo battery and charger
Driver used: bq27441
Example:
    >> bat = JemBattery()
    >> bat.voltage
    >> 3.4
    >> bat.current_average
    >> 100.1 # mA
    >> bat.soc
    >> 50 # % charge battery remaining
    >> bat.power_down() # power down the fuel gauge - not recommended
    >> bat.pn # part number of driver
    >> "bq27441"
    >> bat.interface # type of communication
    >> "i2c"
"""

from drivers.bq27441 import BQ27441, CurrentMeasureType, CapacityMeasureType, SohMeasureType

class JemBattery(BQ27441):
    def __init__(self, i2c=None):
        """Initialize JemDevice parent class and then set the comm and bq27441 driver objects"""
        super(JemBattery, self).__init__(i2c=i2c, address=BQ27441.I2C_ADDRESS)

    @property
    def current_average(self):
        """Return average current"""
        try:
            result = self.current(CurrentMeasureType.AVG)
            return result
        except Exception as e:
            print("Failed to get average current (mA): %s" % e)

    @property
    def capacity_full(self):
        """Return full capacity (mAh)"""
        try:
            result = self.capacity(CapacityMeasureType.FULL)
            return result
        except Exception as e:
            print ("Failed to get max capacity (mAh): %s" % e)

    @property
    def capacity_remaining(self):
        """Return remaining capacity (mAh)"""
        try:
            result = self.capacity(CapacityMeasureType.REMAIN)
            return result
        except Exception as e:
            print ("Failed to get average current (mA): %s" % e)

    @property
    def soh(self):
        """Return state of health"""
        try:
            result = self._device.soh(SohMeasureType.PERCENT)
            return result
        except Exception as e:
            print ("Failed to get state of health (soh): %s" % e )
