# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from ble_uart_repl import BLEUARTStream
from ble_uart_peripheral import BLEUART, BLE
from ble_uart_ftp import BLEUARTFTP
from ble_uart_remote_control import BLEUARTREMOTECONTROL
from ble_info_service import BLEINFOService
from machine import Timer
import bluetooth
import os
import json

esp32_ble = bluetooth.BLE()
name="JEM-BLE"
try:
    with open("jem_config.json", "r") as f:
        json_str = f.read()
        json_config = json.loads(json_str)
        name = json_config['ble']['name'] #get ble adv name
except Exception as e:
    print("BLEMANAGER: Failed to load jem_config.json: %s" % e)

try:
    jem_ble = BLE(esp32_ble, name=name)

    repl_uart = BLEUART(jem_ble, service_uuid="6E400001-B5A3-F393-E0A9-E50E24DCCA9E",
                            tx_chr_uuid="6E400003-B5A3-F393-E0A9-E50E24DCCA9E",
                            rx_chr_uuid="6E400002-B5A3-F393-E0A9-E50E24DCCA9E", primary=True)
    ble_repl = BLEUARTStream(Timer(0), repl_uart)

    ftp_uart = BLEUART(jem_ble, service_uuid="6E400001-B5A3-F393-E0A9-E50E24DCCA77",
                            tx_chr_uuid="6E400003-B5A3-F393-E0A9-E50E24DCCA77",
                            rx_chr_uuid="6E400002-B5A3-F393-E0A9-E50E24DCCA77")
    ftp = BLEUARTFTP(Timer(1), ftp_uart)

    rc_uart = BLEUART(jem_ble, service_uuid = 0xCA33, rx_chr_uuid = 0xCB33, tx_chr_uuid = 0xCC33)
    rc = BLEUARTREMOTECONTROL(Timer(2), rc_uart)


    info = BLEINFOService(jem_ble, service_uuid=0xABCD)
except Exception as e:
    print("boot failed %s" % e)
    print("Attempting to start ble anyhow")

jem_ble.add_connect_callback(ble_repl.connected_event)
jem_ble.add_connect_callback(info.notify_mtu)
jem_ble.advertise()


#IRQ_MTU_EXCHANGED
print("jem ble adv!")
