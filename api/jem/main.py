# #main.py
# #from kits import kit_main
# #kit_main.load_kit()]
# from jemwifi import *
# from jem_help import jem_help
# from jemled import *
# from jembuzzer import *
# from jemrange import *
# from drivers.pcf8574 import *
#
# global wlan
# wlan = setup_wifi('purple_rain')
#
# from machine import Pin, I2C
#
# # p9 = sda, p10 = scl
# i2c = I2C(0, I2C.MASTER, pins=('p9', 'p10'), baudrate=4000)
# pcf8574 = PCF8574(i2c, addr=0x20)
#
# # test out different combinations of 0b10101010
#
# def forward():
#     pcf8574.outputs(0b10101010) # you need to change these
#
# def backward():
#     pcf8574.outputs(0b10101010)
#
# def left():
#     pcf8574.outputs(0b10101010)
#
# def right():
#     pcf8574.outputs(0b10101010)
#
#
# #kit = Kit()
# #kit.start()
# RED = 0x880000 # red, green blue
# GREEN = 0x008800
# BLUE = 0x000088
# PURPLE = 0x440088
# PINK = 0x880080
# YELLOW = 0x111100
# jem_led = JemLed()
# jem_buzz = JemBuzzer()
# jem_range = JemRange()
#
# def color(c = RED):
#     jem_led.set_color(c)
#
# def buzz(freq=100):
#     if freq == 0:
#         jem_buzz.stop()
#     else:
#         jem_buzz.start(freq)
#
# def distance():
#     print("%s" % jem_range.distance)
from kits.kit import Kit

kit = Kit()
kit.start()
