#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
from jem_help import jem_help
from drivers.peripherals import JemI2C, I2C, JEM_DEFAULT_I2C_BUS, JEM_DEFAULT_I2C_BAUDRATE, JEM_DEFAULT_I2C_PINS

global wlan
wlan = setup_wifi()

from drivers.pcf8574 import *

from machine import Pin, I2C

# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
i2c = I2C(JEM_DEFAULT_I2C_BUS, I2C.MASTER, pins=JEM_DEFAULT_I2C_PINS, baudrate=JEM_DEFAULT_I2C_BAUDRATE)
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
