# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).
from network import Bluetooth
import binascii

def uuid2bytes(uuid):
    uuid = uuid.encode().replace(b'-',b'')
    tmp = binascii.unhexlify(uuid)
    return bytes(reversed(tmp))

class BLEUART:
    def __init__(self, ble=Bluetooth(mtu=200), name="JEM", connect_status_handler=None, service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E", rx_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E", tx_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"):
        self._ble = ble
        self._ble.set_advertisement(name='JEM', service_uuid=uuid2bytes(service_uuid))
        self._ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.connected_callback)
        self._ble.advertise(True)
        self.service = self._ble.service(uuid=uuid2bytes(service_uuid), isprimary=True, nbr_chars=2)
        self.rx_characteristic = self.service.characteristic(uuid=uuid2bytes(rx_uuid))
        self.rx_callback = self.rx_characteristic.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=self.rx_cb_handler)
        self.tx_characteristic = self.service.characteristic(uuid=uuid2bytes(tx_uuid))
        self._connected = False
        self._rx_buffer = bytearray()
        self._connect_status_handler = None
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.

    def set_connect_handler(self, handler):
        self._connect_status_handler = handler

    def rx_cb_handler(self, chr, data=None):
        events = chr.events()
        if  events & Bluetooth.CHAR_WRITE_EVENT:
            self._rx_buffer += chr.value()

    def connected_callback(self, bt_o):
        events = bt_o.events()
        if  events & Bluetooth.CLIENT_CONNECTED:
            self._connected = True
            print("ble_uart_peripheral connected")
            if self._connect_status_handler:
                self._connect_status_handler(self._connected)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            self._connected = False
            print("ble_uart_peripheral connected")
            if self._connect_status_handler:
                self._connect_status_handler(self._connected)

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        if self._connected:
            self.tx_characteristic.value(data)
