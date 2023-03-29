
from kits.kit import Kit

#kit = Kit()
#kit.start()
from kits.simplebot.simplebot import SimpleBot
from machine import Pin, PWM
bot = SimpleBot(en_pin=Pin(33,Pin.OUT), left_pwm=PWM(Pin(2)), right_pwm=PWM(Pin(14)))
