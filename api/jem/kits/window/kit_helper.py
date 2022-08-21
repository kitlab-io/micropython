import json, pycom, time
from ble_uart_peripheral import BLEMANAGER
from drivers.neopixel import Neopixel
from jem import Jem

WINDOW_PIXEL_COUNT = 8*8 # 64 pixels

# singleton object
class KitHelper:
    def __init__(self):
        self.board = Jem()
        self.neopixel = Neopixel(num_leds=WINDOW_PIXEL_COUNT)
        self.bleManager = BLEMANAGER()
        print("KitHelper init")

    def connected(self):
        return self.bleManager.is_connected()

class KitHelperManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None: # just init once (KitHelper is a singleton)
            print("creatig new KitHelper")
            cls._instance = KitHelper()
        return cls._instance

    def connected(self):
        return self.bleManager.is_connected()

kit_helper = KitHelperManager()
