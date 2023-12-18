from machine import Pin, I2C, PWM
from drivers.pcf8574 import *
import time

class Car:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=100000) #100khz
        self.pcf8574 = PCF8574(self.i2c, addr=0x20)
        # Initialize PWM for motor speed control
        # Assuming PWM capable pins are connected to L293D's enable pins
        # Set initial PWM frequency (for example, 1000 Hz)
        self.pwmA = PWM(Pin(4),1000)  
        self.pwmB = PWM(Pin(14),1000)  
        self.pwmC = PWM(Pin(21),1000)  
        self.pwmD = PWM(Pin(22),1000)
        self.speed=512
    def set_speed(self, speed=512):
        # Speed is a value between 0 and 1023 (for 10-bit resolution)
        self.pwmA.duty(speed)
        self.pwmB.duty(speed)
        self.pwmC.duty(speed)
        self.pwmD.duty(speed)
        self.speed=speed
    def forward(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b10010110) # forward
        print("forward")
        #time.sleep(2)
        #self.stop()
    def backward(self):
      	self.set_speed(self.speed)
        self.pcf8574.outputs(0b01101001) # backward
        print("back")
        #time.sleep(2)
        #self.stop()
    def spin_right(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b01010101) # spin right
        print("right")
        #time.sleep(2)
        #self.stop()
    def spin_left(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b10101010) # spin left
        print("left")
        #time.sleep(2)
        #self.stop()
    def strafe_right(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b10100101) # strafe right
        print("strafe right")
        #time.sleep(2)
        #self.stop()
    def strafe_left(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b01011010) # strafe left
        print("strafe left")
        #time.sleep(2)
        #self.stop()
    def forward_right(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b10000100) # forward right
        print("forward right")
        #time.sleep(2)
        #self.stop()
    def forward_left(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b00010010) # forward left
        print("forward left")
        #time.sleep(2)
        #self.stop()
    def backward_left(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b01001000) # backward left
        print("backward left")
        #time.sleep(2)
        #self.stop()
    def backward_right(self):
        self.set_speed(self.speed)
        self.pcf8574.outputs(0b00100001) # backward right
        print("backward right")
        #time.sleep(2)
        #self.stop()
    def stop(self):
        self.pcf8574.outputs(0b00000000) # stop

car = Car()


def run():
    print("rc car started")

# print("worked")
#
# from machine import PWM
# pwm_1 = PWM(0, frequency=500)  # use PWM timer 0, with a frequency of 5KHz
# pwm_2 = PWM(1, frequency=500)  # use PWM timer 0, with a frequency of 5KHz
# pwm_3 = PWM(2, frequency=500)  # use PWM timer 0, with a frequency of 5KHz
# pwm_4 = PWM(3, frequency=500)  # use PWM timer 0, with a frequency of 5KHz
# # create pwm channel on pin P12 with a duty cycle of 50%
# pwm_a = pwm_1.channel(0, pin='P19', duty_cycle=0.9)
# pwm_a.duty_cycle(0.3) # change the duty cycle to 30%
# pwm_b = pwm_2.channel(1, pin='P20', duty_cycle=0.9)
# pwm_b.duty_cycle(0.3) # change the duty cycle to 30%
# pwm_c = pwm_3.channel(2, pin='P12', duty_cycle=0.9)
# pwm_c.duty_cycle(0.3) # change the duty cycle to 30%
# pwm_d = pwm_4.channel(3, pin='P11', duty_cycle=0.9)
# pwm_d.duty_cycle(0.3) # change the duty cycle to 30%

# pcf8574.outputs(0b00000000) # stop
# pcf8574.outputs(0b10101010) # spin left
# pcf8574.outputs(0b01010101) # spin right
# pcf8574.outputs(0b01011010) # strafe left
# pcf8574.outputs(0b10100101) # strafe right
# pcf8574.outputs(0b10010110) # forward
# pcf8574.outputs(0b01101001) # backward
# pcf8574.outputs(0b00010010) # forward left
# pcf8574.outputs(0b10000100) # forward right
# pcf8574.outputs(0b01001000) # backward left
# pcf8574.outputs(0b00100001) # backward right
