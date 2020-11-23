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
print("Intensity =", shine.get_analog_value())    # returns value 0-4095
"""

from machine import ADC


class TEMT6000:
    ADC_GPIO_PIN = 'P18'

    def __init__(self, pin_num=ADC_GPIO_PIN):
        self.adc = ADC()
        self.pin_num = pin_num
        # init pin and attenuation value of 11DB (increases adc max input ability to 3.3V)
        self.apin = self.adc.channel(pin=self.pin_num, attn=ADC.ATTN_11DB)
        
    def get_analog_value(self):
        """returns value 0 - 4095"""
        an = self.apin()
        return an

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
