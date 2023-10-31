# FTP over BLE UART
from cmd import *

class BLEUARTFTP:
    def __init__(self, uart):
        self._uart = uart
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

    def write(self, buf):
        self._uart.write(buf)
