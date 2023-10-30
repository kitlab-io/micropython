from jem import jemled, jembuzzer
from ble_uart_peripheral import JEMBLE
import time
import micropython

ble = JEMBLE() # grab global BLE handler
led = jemled.JemLed()
ext_char = None

def led_red():
    led.set_color((100, 0, 0))

def led_blue():
    led.set_color((0, 0, 100))

# jem will call the 'run' method in a thread
# put your kit specific behavior here if you want and it will run in background
# try not to use print in the while loop unless it's to print an error

# in repl, you can set running to False to disable the run function below
running = True 

def write(data):
    global ext_char
    ble.t_write(ext_char, data)
    
def run():
    global ext_char
    print("Demo Kit starting")
    # remote controller ble service
    # the ble service that your demo.vue can use to receive kit specific info from JEM
    rc_uart = ble.get_service_by_name('rc_uart')
    # an extra ble characteristic used by kit to notify mobile app of useful info, like sensor data
    ext_char = rc_uart.get_char_by_name('extra')  
    while running:
        try:
            time.sleep(5)
            write(b'hello from demo kit!')
        except Exception as e:
            print("demo kit run failed: %s" % e)
            break # make sure to exit !
