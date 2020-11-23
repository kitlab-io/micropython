from app.servo import Servo
from machine import Pin
class Robot:
    def __init__(self):
        self.vcc_en = Pin('P20', mode=Pin.OUT)
        self.left_motor = Servo(id=1, pwm_pin='P21', reverse=True)
        self.right_motor = Servo(id=2, pwm_pin='P22')

    def start(self):
        self.vcc_en.value(1)

    def stop(self):
        self.vcc_en.value(0)

    def turn_left(self, speed=50):
        self.left_motor.drive(speed)

    def turn_right(self, speed=50):
        self.right_motor.drive(speed)

    def forward(self, speed=50):
        self.right_motor.drive(speed)
        self.left_motor.drive(speed)

    def backward(self, speed=50):
        self.right_motor.drive(-1*speed)
        self.left_motor.drive(-1*speed)

    def move(self, left_speed=0, right_speed=0):
        self.left_motor.drive(left_speed)
        self.right_motor.drive(right_speed)
