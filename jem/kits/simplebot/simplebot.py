from kits.simplebot.servo import Servo
from machine import Pin, PWM

class SimpleBot:
    def __init__(self, en_pin, left_pwm, right_pwm):
        self.vcc_en = en_pin
        self.left_motor = Servo(pwm=left_pwm, reverse=True, name="left")
        self.right_motor = Servo(pwm=right_pwm, name="right")

    def start(self):
        print("start")
        self.vcc_en.value(1)

    def stop(self):
        print("stop")
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

# run method will be called inside thread by main.py
# put your kit main code here - it will run in parallel to the micropython repl

class PwmWrapper:
    def __init__(self, pin, pwm_freq_hz=50):
        self.pwm = PWM(Pin(pin), freq=pwm_freq_hz, duty=0)

    def duty_percent(self, duty):
        # ex: 100% = 1023 (max of 2**10 - 1)
        # duty = pwm.duty()         # get current duty cycle, range 0-1023 (default 512, 50%)
        # pwm.duty(256)             # set duty cycle from 0 to 1023 as a ratio duty/1023, (now 25%)
        print("duty_percent %s" % duty)
        self.pwm.duty(int(duty * (1023.0 / 100.0)))  # 10 bit max (0 - 1023)))
        print("%s" % self.pwm.duty())

    def freq(self, freq):
        # ex freq hz
        # freq = pwm.freq()  # get current frequency hz
        # pwm.freq(1000) # set to 1000 hz
        print("req = %s" % (freq))
        self.pwm.freq(freq)

global robot

en_pin = Pin(33, mode=Pin.OUT) # enable power to servos
left_servo = PwmWrapper(pin=2)
right_servo = PwmWrapper(pin=14)
robot = SimpleBot(en_pin, left_servo, right_servo)

def run():
    # add your code here
    print("SimpleBot start, nothing to do except use the mobile App")


