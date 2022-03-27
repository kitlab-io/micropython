# FTP over BLE UART
from machine import Timer
from ble_uart_peripheral import BLEUART
from cmd import *

class BLEUARTFTP:
    def __init__(self, uart=None):
        if uart is None:
            uart = BLEUART(name="BLEUARTFTP", service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA77", rx_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA77", tx_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA77")
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self._uart.set_connect_handler(self.on_connect_status_changed)
        self.prev_term = None
        self._timer = None
        self._uart.set_rx_notify_callback(self.rx_notification)
        self.ftp_cmd_manager = CmdManager()

    def _wrap_flush(self, alarm):
        self._flush()

    def schedule_tx(self):
        self._timer = Timer.Alarm(self._wrap_flush, ms=self.tx_delay_ms, periodic=False)

    def on_connect_status_changed(self, is_connected):
        if is_connected:
            print("BLEUARTFTP - CONNECTED")
        else:
            print("BLEUARTFTP - DISCONNECTED")

    def read(self, sz=None):
        return self._uart.read(sz)

    def rx_notification(self):
        # we got some data!
        try:
            data = self.read()
            self.update(data)
            #print("rx_notification: %s" % data)
        except Exception as e:
            print("BLEUARTFTP rx_notification failed - %s" % e)

    def update(self, data):
        resp = self.ftp_cmd_manager.update(data)
        if resp:
            self.write(resp)

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
