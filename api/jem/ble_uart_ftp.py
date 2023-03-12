# FTP over BLE UART
from ble_uart_peripheral import schedule_in
from cmd import *

class BLEUARTFTP:
    def __init__(self, tmr, uart):
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self._timer = tmr
        self._uart.irq(self._on_rx)
        self.ftp_cmd_manager = CmdManager()

    def on_connect_status_changed(self, is_connected):
        if is_connected:
            print("BLEUARTFTP - CONNECTED")
        else:
            print("BLEUARTFTP - DISCONNECTED")

    def read(self, sz=None):
        return self._uart.read(sz)

    def _on_rx(self):
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
            schedule_in(self._timer, self._flush, self.tx_delay_ms)

    def write(self, buf):
        empty = not self._tx_buf
        self._tx_buf += buf
        if empty:
            schedule_in(self._timer, self._flush, self.tx_delay_ms)
