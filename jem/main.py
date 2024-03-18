from kits.kit import Kit
from ble_uart_peripheral import JEMBLE
ble = JEMBLE()
rc_uart = ble.get_service_by_name('rc_uart')
ext_char = rc_uart.get_char_by_name('extra')

kit = Kit()
#kit.start()

kit._kit.car.stop() # stop car on startup just in case

def connected_cbk(c):
    print("connected_cbk %s" % c)
    # stop motors if newly connected or disconnected
    kit._kit.car.stop()
    
ble.add_connect_callback(connected_cbk) # if ble connected / disconnecs we will know

def mtr(output, pwma, pwmb, pwmc, pwmd):
    global ext_char
    global ble
    try:
        kit._kit.car.update(output, pwma, pwmb, pwmc, pwmd)
    except Exception as e:
        print(e)
    ble.write(ext_char, b'r') # notify app we are ready again for another mtr control ('r') 
