# Proof-of-concept of a REPL over BLE UART.
#
# Tested with the Adafruit Bluefruit app on Android.
# Set the EoL characters to \r\n.

import io
import os

_MP_STREAM_POLL = const(3)
_MP_STREAM_POLL_RD = const(0x0001)

# Simple buffering stream to support the dupterm requirements.
class BLEUARTStream(io.IOBase):
    def __init__(self, uart):
        self._uart = uart # ble_uart_peripheral.py BLEUART object
        self._uart.irq(self._on_rx)
        self.errors = []

    def connected_event(self, connected):
        if connected:
            os.dupterm(self)
        else:
            os.dupterm(None)

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

    def write(self, buf):
        try:
            self._uart.write(buf)
        except Exception as e:
            self.errors.append(e)
