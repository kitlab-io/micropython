from kits.simplebot.servo import Servo
from machine import Pin, PWM

class SimpleBot:
    def __init__(self, en_pin, left_pwm, right_pwm):
        self.vcc_en = en_pin
        self.left_motor = Servo(pwm=left_pwm, reverse=True, name="left")
        self.right_motor = Servo(pwm=right_pwm, name="right")

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

# run method will be called inside thread by main.py
# put your kit main code here - it will run in parallel to the micropython repl
class FakePin:
    def value(self, v):
        print("value = %s" % v)

class FakePwm:
    def __init__(self, name):
        self.name = name

    def duty_percent(self, duty):
        print("%s duty = %s" % (self.name, duty))

    def freq(self, freq):
        print("%s freq = %s" % (self.name, freq))

class PwmWrapper:
    def __init__(self, id, pin, pwm_freq_hz=50):
        self._pwm = PWM(id, frequency=pwm_freq_hz)
        self.pwm_c = self._pwm.channel(id, pin=pin, duty_cycle=0.0)

    def duty_percent(self, duty):
        self.pwm_c.duty_cycle(duty/100.0) # percent at franction ex 0.3 -> 30%

    def freq(self, freq):
        print("req = %s" % (freq))

global robot

#robot = SimpleBot(FakePin(), FakePwm("left"), FakePwm("right"))
robot = SimpleBot(Pin('P6', mode=Pin.OUT), PwmWrapper(id=1, pin='P11'), PwmWrapper(id=2, pin='P12'))

def run():
    print("SimpleBot start, nothing to do except use the mobile App")
