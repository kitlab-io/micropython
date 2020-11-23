#Raspberry Pi TB6612FNG Library
from machine import Pin, PWM
hertz = 1000
class TB6612FNG_Motor:
	#Constructor
	def __init__(self, motor_id=1, in1='P20', in2='P21', pwm_pin='P22', standbyPin=None, reverse=False):
		if motor_id == 2:
			in2 = 'P11'
			pwm_pin = 'P2'
			in1 = 'P19'
		self.in1 = Pin(in1, mode=Pin.OUT)
		self.in2 = Pin(in2, mode=Pin.OUT)
		self.pwm = PWM(motor_id, frequency=hertz)  # use PWM timer 0, with a frequency of 5KHz
		self.pwm_c = self.pwm.channel(motor_id, pin=pwm_pin, duty_cycle=0.0)
		self.reverse = reverse
		if standbyPin:
			self.standbyPin = Pin(standbyPin, mode=Pin.OUT)
		else:
			self.standbyPin = None
		if standbyPin:
			self.standbyPin.value(1)
	#Speed from -100 to 100
	def drive(self, speed):
		#Negative speed for reverse, positive for forward
		#If necessary use reverse parameter in constructor
		dutyCycle = speed
		if(speed < 0):
			dutyCycle = dutyCycle * -1
		if(self.reverse):
			speed = speed * -1
		if(speed > 0):
			self.in1.value(1)
			self.in2.value(0)
		else:
			self.in1.value(0)
			self.in2.value(1)

		self.pwm_c.duty_cycle(dutyCycle/100.0)

	def brake(self):
		self.pwm_c.duty_cycle(0)
		self.in1.value(1)
		self.in2.value(1)

	def standby(self, value):
		self.pwm_c.duty_cycle(0)
		if self.standbyPin:
			self.standbyPin.value(value)
