from machine import Pin, I2C
from drivers.pcf8574 import *
import time

class Car:
    def __init__(self):
        self.i2c = I2C(0, I2C.MASTER, pins=('P9', 'P10'), baudrate=4000)
        self.pcf8574 = PCF8574(self.i2c, addr=0x20)
    def forward(self):
        self.pcf8574.outputs(0b01011010) # forward
        print("forward")
        time.sleep(2)
        self.stop()
    def backward(self):
        self.pcf8574.outputs(0b10100101) # backward
        print("back")
        time.sleep(2)
        self.stop()
    def right(self):
        self.pcf8574.outputs(0b01010101) # spin right
        print("right")
        time.sleep(2)
        self.stop()
    def left(self):
        self.pcf8574.outputs(0b10101010) # spin left
        print("left")
        time.sleep(2)
        self.stop()
    def stop(self):
        self.pcf8574.outputs(0b00000000) # stop

    def move(self, left_speed=0, right_speed=0):
        self.left_motor.drive(left_speed)
        self.right_motor.drive(right_speed)


car = Car()


def run():
    print("rc car started")





# pcf8574.outputs(0b00000000) # stop
# pcf8574.outputs(0b10101010) # spin left
# pcf8574.outputs(0b01010101) # spin right
# pcf8574.outputs(0b01011010) # forward
# pcf8574.outputs(0b10100101) # backward
# pcf8574.outputs(0b10010110) # strafe left
# pcf8574.outputs(0b01101001) # strafe right
# pcf8574.outputs(0b00010010) # forward left
# pcf8574.outputs(0b01001000) # forward right
# pcf8574.outputs(0b10000100) # backward left
# pcf8574.outputs(0b00100001) # backward right
