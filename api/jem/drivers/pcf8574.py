# pcf8574.py
# 8-bit I/O expander code for PN: PCF8574
from machine import I2C

class PCF8574:
# PCF8574 default address.
# I2C_ADDRESS = 0x20

    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.addr = addr
        self._output_state = 0xFF

    def _write_byte(self, value):
        # Write a byte to the PCF8574
        self.i2c.writeto(self.addr, bytes([value]))
        self._output_state = value

    def _read_byte(self):
        # Read a byte from the PCF8574
        return self.i2c.readfrom(self.addr, 1)[0]

    def output(self, pin, value):
        # Set the output state of a single pin
        if value:
            self._output_state |= 1 << pin
        else:
            self._output_state &= ~(1 << pin)
        self._write_byte(self._output_state)

    def input(self, pin):
        # Read the input state of a single pin
        input_state = self._read_byte()
        return (input_state >> pin) & 1

    def outputs(self, value):
        # Set the output state of all pins
        self._write_byte(value)
        self._output_state = value

    def inputs(self):
        # Read the input state of all pins
        input_state = self._read_byte()
        return input_state

# Example of use:
# To use this driver, create an instance of the PCF8574 class,
# passing in the I2C bus object and the address of the PCF8574 chip.
# Then, call the output() method to set the output state of a single pin,
# or the inputs() method to read the input state of all pins.
#
# Here's an example of how to use the driver to set the output state
# of all pins to 0b10101010, and then read the input state of pin 3:
"""
from machine import Pin, I2C

i2c = I2C(0, I2C.MASTER, pins=('P9', 'P10'), baudrate=4000)
pcf8574 = PCF8574(i2c, addr=0x20)

pcf8574.outputs(0b00000000) # stop
pcf8574.outputs(0b10101010) # spin left
pcf8574.outputs(0b01010101) # spin right
pcf8574.outputs(0b01011010) # forward
pcf8574.outputs(0b10100101) # backward
pcf8574.outputs(0b10010110) # strafe left
pcf8574.outputs(0b01101001) # strafe right
pcf8574.outputs(0b00010010) # forward left
pcf8574.outputs(0b01001000) # forward right
pcf8574.outputs(0b10000100) # backward left
pcf8574.outputs(0b00100001) # backward right
input_state = pcf8574.input(3)
print("Input state of pin 3: {}".format(input_state))
"""
