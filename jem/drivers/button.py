"""button.py
Driver: button
Desc: Detect button press, if button press time > 3 sec then JEM will be powered down
      so developer can use button to gracefully shutdown system before power goes out by using this driver
      or just use for general purpose control but just be aware of the 3 sec power down press
ex:
>> from drivers.button import *
>> b = Button() # uses jem2 IO39 / SENSOR_VN by default
>> b.read()

>> # use different gpio than default
>> b12 = Button(pin_num=12)
>> b12.read()
"""

from machine import Pin

class Button:
    BUTTON_GPIO_PIN = 39 # default jem2 button SENSOR_VN on esp32 wrover E
    GPIO_PIN_PULL = None # ex: Pin.PULL_UP, Pin.PULL_DOWN
    def __init__(self, pin_num=BUTTON_GPIO_PIN, pin_pull=GPIO_PIN_PULL):
        self.pin = Pin(pin_num, mode=Pin.IN, pull=pin_pull)

    def read(self):
        return self.pin.value()
