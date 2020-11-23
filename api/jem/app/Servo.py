#Servo.py
from machine import Pin, PWM
# Position "90" (1.5ms pulse) is stop, "180" (2ms pulse) is full speed forward, "0" (1ms pulse) is full speed backwards
#Servo2 (right):
#P22 (purple) -> PWM1
#Servo1 (left):
#P21 -> PWM2
#P20 -> VCC_EN

class Servo:
	def __init__(self, id, pwm_pin, reverse=False, pwm_freq_hz=50):
		self.pwm = PWM(id, frequency=pwm_freq_hz)
		self.pwm_c = self.pwm.channel(id, pin=pwm_pin, duty_cycle=0.0)
		self.reverse = reverse
		self.stop_pw= 1.5
		self.forward_pw = 2.0
		self.backward_pw = 1.0
		self.period_ms = 1000.0/float(pwm_freq_hz) #if hertz 50 then period = 20 ms
		self.name="Servo"

	def drive(self, speed):
		if self.reverse:
			speed = -1*speed
		if abs(speed) > 100:
			speed = 100

		pw = (1/200.0)*speed + 1.5
		duty_cycle = pw / self.period_ms
		self.pwm_c.duty_cycle(duty_cycle)
		return duty_cycle
