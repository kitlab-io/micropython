# Proof-of-concept of a Kit Remote Control over BLE UART
from machine import Timer
from ble_uart_peripheral import BLEUART
from ftp_cmd import *


class BLEUARTREMOTECONTROL:
    def __init__(self, uart=None):
        if uart is None:
            uart = BLEUART(name="BLEUARTREMOTECONTROL", service_uuid = 0xCA33, rx_uuid = 0xCB33, tx_uuid = 0xCC33, aux_uuid = 0xCD33)
        self._uart = uart
        self._tx_buf = bytearray()
        self._aux_tx_buf = bytearray() # used for sending extra data from Kit to App (like asynchronous sensor data)
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self.cmd_delay_ms = 1
        self._uart.set_connect_handler(self.on_connect_status_changed)
        self.prev_term = None
        self._timer = None
        self._aux_timer = None
        self._cmd_timer = None
        self._cmd_queue = []
        self._uart.set_rx_notify_callback(self.rx_notification)

    def _wrap_flush(self, alarm):
        self._flush()

    def _wrap_aux_flush(self, alarm):
        self._aux_flush()

    def schedule_tx(self):
        self._timer = Timer.Alarm(self._wrap_flush, ms=self.tx_delay_ms, periodic=False)

    def schedule_aux_tx(self):
        self._aux_timer = Timer.Alarm(self._wrap_aux_flush, ms=self.tx_delay_ms, periodic=False)

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
            resp = self.queue_cmd(data)
            if resp:
                self.write(resp)
        except Exception as e:
            print("BLEUARTREMOTECONTROL rx_notification failed: %s" % e)

    def queue_cmd(self, data):
        try:
            resp = "ok"
            code = data.decode("utf-8") # convert to string instead of byte array
            self._cmd_queue.append(code)
            self.schedule_cmd()
        except Exception as e:
            resp = "queue_cmd failed: %s" % e
            print(resp)
        return resp

    def schedule_cmd(self):
        self._cmd_timer = Timer.Alarm(self._wrap_cmd, ms=self.cmd_delay_ms, periodic=False)

    def _wrap_cmd(self, alarm):
        self._execute_next_cmd()

    def _execute_next_cmd(self):
        #cmd_handler is called when the RemoteControlBleService receives a valid message from the App over BLE
        try:
            if not self._cmd_queue:
                return
            code = self._cmd_queue.pop()
            eval(code) # example: eval("move(50,40)") will move car left =50, right=40
        except Exception as e:
            print("_cmd failed: %s" % e)
        if self._cmd_queue:
            self.schedule_cmd()
        return

    def _flush(self):
        data = self._tx_buf[0:self.tx_max_len]
        self._tx_buf = self._tx_buf[self.tx_max_len:]
        self._uart.write(data)
        if self._tx_buf:
            self.schedule_tx()

    def _aux_flush(self):
        data = self._aux_tx_buf[0:self.tx_max_len]
        self._aux_tx_buf = self._aux_tx_buf[self.tx_max_len:]
        self._uart.write_aux(data)
        if self._aux_tx_buf:
            self.schedule_aux_tx()

    def write(self, buf):
        empty = not self._tx_buf
        self._tx_buf += buf
        if empty:
            self.schedule_tx()

    def write_aux(self, buf):
        empty = not self._aux_tx_buf
        self._aux_tx_buf += buf
        if empty:
            self.schedule_aux_tx()
