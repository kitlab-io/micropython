# Proof-of-concept of a Kit Remote Control over BLE UART
from machine import Timer
from ble_uart_peripheral import BLEUART
from ftp_cmd import *


class BLEUARTREMOTECONTROL:
    def __init__(self, uart=None):
        if uart is None:
            uart = BLEUART(name="BLEUARTREMOTECONTROL", service_uuid = 0xCA33, rx_uuid = 0xCB33, tx_uuid = 0xCC33)
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self._uart.set_connect_handler(self.on_connect_status_changed)
        self.prev_term = None
        self._timer = None
        self._uart.set_rx_notify_callback(self.rx_notification)

    def _wrap_flush(self, alarm):
        self._flush()

    def schedule_tx(self):
        self._timer = Timer.Alarm(self._wrap_flush, ms=self.tx_delay_ms, periodic=False)

    def on_connect_status_changed(self, is_connected):
        if is_connected:
            print("BLEUARTREMOTECONTROL - CONNECTED")
        else:
            print("BLEUARTREMOTECONTROL - DISCONNECTED")

    def read(self, sz=None):
        return self._uart.read(sz)

    def rx_notification(self):
        # we got some data!
        try:
            data = self.read()
            resp = self.cmd_handler(data)
            if resp:
                self.write(resp)
        except Exception as e:
            print("BLEUARTREMOTECONTROL rx_notification failed: %s" % e)

    def cmd_handler(self, data):
        #cmd_handler is called when the RemoteControlBleService receives a valid message from the App over BLE
        resp = "ok"
        try:
            code = data.decode("utf-8") # convert to string instead of byte array
            eval(code) # example: eval("move(50,40)") will move car left =50, right=40
        except Exception as e:
            resp = "cmd_handler failed: %s" % e
            print(resp)
        return resp

    def _flush(self):
        data = self._tx_buf[0:self.tx_max_len]
        self._tx_buf = self._tx_buf[self.tx_max_len:]
        self._uart.write(data)
        if self._tx_buf:
            self.schedule_tx()

    def write(self, buf):
        empty = not self._tx_buf
        self._tx_buf += buf
        if empty:
            self.schedule_tx()
