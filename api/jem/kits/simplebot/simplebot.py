from kits.simplebot.servo import Servo

class SimpleBot:
    def __init__(self, en_pin, left_pwm, right_pwm):
        self.vcc_en = en_pin
        self.left_motor = Servo(pwm=left_pwm, reverse=True)
        self.right_motor = Servo(pwm=right_pwm)

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
        printf("value = %s" % v)

class FakePwm:
    def __init__(self, name):
        self.name = name

    def duty(self, duty):
        print("%s duty = %s" % (self.name, duty))

    def freq(self, freq):
        print("%s freq = %s" % (self.name, freq))

global robot
robot = SimpleBot(FakePin(), FakePwm("left"), FakePwm("right"))

def run():
    print("SimpleBot start, nothing to do except use the mobile App")
