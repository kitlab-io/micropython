"""temt6000.py
Driver: temt6000
Desc: Ambient light sensor. Acts like transistor - the greater the incoming light the higher
the analog voltage on the signal pin

Communication Interface:   I2C
WiPy 2.0 connections:
pycom           temt6000
GND     <<< >>> GND
3V3     <<< >>> 3V3
P18     <<< >>> SIG

USAGE
>> from drivers.temt6000 import *
>> light = TEMPT6000()
print("Intensity =", light.get_analog_value())    # returns value 0-4095
"""

from machine import ADC, Pin


class TEMT6000:
    # jem-2 esp32 IO36 is SENSOR_VP
    ADC_GPIO_PIN = 36

    def __init__(self, pin_num=ADC_GPIO_PIN):
        self.pin_num = pin_num
        self.adc = ADC(Pin(self.pin_num, Pin.IN)) # 12 bit
        self.adc.init(atten=ADC.ATTN_11DB) # 11dB attenuation (150mV - 2450mV)

    def get_analog_value(self):
        """returns 12 bit value 0 - 4095"""
        return self.adc.read()

    def get_voltage(self):
        """returns voltage 0 - 3.3V"""
        an = self.get_analog_value()
        volts = an * (3.3 / 4095)
        return volts

    def get_intensity(self):
        """return value 0 - 100%"""
        analog = self.get_analog_value()
        percent = analog / 4095.0
        return percent

    @property
    def intensity(self):
        return self.get_intensity()

    @property
    def voltage(self):
        return self.get_voltage()

    @property
    def analog(self):
        return self.get_analog_value()
