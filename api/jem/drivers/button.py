"""button.py
Driver: button
Desc: Detect button press, if button press time > 3 sec then JEM will be powered down
      so developer can use button to gracefully shutdown system before power goes out by using this driver
      or just use for general purpose control but just be aware of the 3 sec power down press
"""

from machine import Pin

class Button:
    def __init__(self):
        self.pin = Pin('P15', mode=Pin.IN)

    def read(self):
        return self.pin.value()
