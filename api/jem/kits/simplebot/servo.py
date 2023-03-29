#Servo.py
from machine import Pin, PWM
# Position "90" (1.5ms pulse) is stop, "180" (2ms pulse) is full speed forward, "0" (1ms pulse) is full speed backwards
#Servo2 (right):
#P22 (purple) -> PWM1
#Servo1 (left):
#P21 -> PWM2
#P20 -> VCC_EN

# pwm: just has to be any pwm object that has following functions
# set_freq_hz (ex: 50 hz)
# set_duty_percent (ex 50%)


class Servo:
    def __init__(self, pwm, reverse=False, pwm_freq_hz=50):
        self.pwm = pwm
        self.reverse = reverse
        self.stop_pw= 1.5
        self.forward_pw = 2.0
        self.backward_pw = 1.0
        self.period_ms = 1000.0/float(pwm_freq_hz) #if hertz 50 then period = 20 ms
        self.pwm.freq(pwm_freq_hz)

    def drive(self, speed):
        direction = 1
        if self.reverse:
            direction = -1
        if abs(speed) > 100:
            speed = 100

        speed = direction * speed # left / right wheel might need to spin differently
        # calculate pulse width in millisec for servo
        # most servos require pulse width between 1 - 2 millisec to drive
        # 1.5 millisec typically resulting in ZERO movement
        pw_ms = (1/200.0) * speed + 1.5

        # get pwm duty cycle percent (0 - 100%)
        duty = pw_ms / self.period_ms # period_ms is max period of pwm timer
        duty_percent = 100*duty
        # ex: 100% = 1023 (max of 2**10 - 1)
        self.pwm.duty(int(duty_percent * (1023.0/100.0))) # 10 bit max (0 - 1023)))
        return duty_percent
