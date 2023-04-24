#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
from jem_help import jem_help

global wlan
wlan = setup_wifi()

from drivers.pcf8574 import *

from machine import Pin, I2C

# p9 = sda, p10 = scl
i2c = I2C(0, I2C.MASTER, pins=('p9', 'p10'), baudrate=4000)
pcf8574 = PCF8574(i2c, addr=0x20)

# test out different combinations of 0b10101010

def forward():
    pcf8574.outputs(0b10101010) # you need to change these

def backward():
    pcf8574.outputs(0b10101010)

def left():
    pcf8574.outputs(0b10101010)

def right():
    pcf8574.outputs(0b10101010)
