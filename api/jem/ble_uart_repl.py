# Proof-of-concept of a REPL over BLE UART.
#
# Tested with the Adafruit Bluefruit app on Android.
# Set the EoL characters to \r\n.

import io
import os
import machine
from ble_uart_peripheral import schedule_in

_MP_STREAM_POLL = const(3)
_MP_STREAM_POLL_RD = const(0x0001)

# Simple buffering stream to support the dupterm requirements.
class BLEUARTStream(io.IOBase):
    def __init__(self, tmr, uart):
        self._uart = uart # ble_uart_peripheral.py BLEUART object
        self._tx_buf = bytearray()
        self._uart.irq(self._on_rx)
        self.tx_delay_ms = 25
        self._timer = tmr # ex: machine.Timer(0)
    
    def _on_rx(self):
        # Needed for ESP32.
        if hasattr(os, "dupterm_notify"):
            os.dupterm_notify(None)

    def read(self, sz=None):
        return self._uart.read(sz)

    def readinto(self, buf):
        avail = self._uart.read(len(buf))
        if not avail:
            return None
        for i in range(len(avail)):
            buf[i] = avail[i]
        return len(avail)

    def ioctl(self, op, arg):
        if op == _MP_STREAM_POLL:
            if self._uart.any():
                return _MP_STREAM_POLL_RD
        return 0

    def _flush(self):
        data = self._tx_buf[0:100]
        self._tx_buf = self._tx_buf[100:]
        self._uart.write(data)
        if self._tx_buf:
            schedule_in(self._timer, self._flush, self.tx_delay_ms)

    def write(self, buf):
        empty = not self._tx_buf
        self._tx_buf += buf
        if empty:
            schedule_in(self._timer, self._flush, self.tx_delay_ms)

