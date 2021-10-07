# REPL over BLE UART

import uos
from machine import Timer
from ble_uart_peripheral import BLEUART, _UART_SERVICE_UUID, _UART_TX_UUID, _UART_RX_UUID

_MP_STREAM_POLL = const(3)
_MP_STREAM_POLL_RD = const(0x0001)

# Simple buffering stream to support the dupterm requirements.
class BLEUARTStream:
    def __init__(self, uart=None):
        if uart is None:
            uart = BLEUART(name="BLEUARTREPL", service_uuid = _UART_SERVICE_UUID, rx_uuid = _UART_RX_UUID, tx_uuid = _UART_TX_UUID )
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self._uart.set_connect_handler(self.on_connect_status_changed)
        self.prev_term = None
        self._timer = None

    def _wrap_flush(self, alarm):
        self._flush()

    def schedule_tx(self):
        self._timer = Timer.Alarm(self._wrap_flush, ms=self.tx_delay_ms, periodic=False)

    def on_connect_status_changed(self, is_connected):
        if is_connected:
            self.prev_term = uos.dupterm()
            print("BLEUARTStream (REPL) Connected")
            print("old dupterm: %s" % self.prev_term)
            uos.dupterm(self)
        else:
            #removes ble dupterm
            if self.prev_term:
                print("inserting old dupterm %s" % self.prev_term)
                uos.dupterm(self.prev_term)
                print("BLEUARTStream (REPL) Disconnected")

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
