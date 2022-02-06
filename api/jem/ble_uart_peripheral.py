# Peripheral implementing the BLE UART Service
from network import Bluetooth
import time
import binascii
_UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
_UART_RX_UUID =      "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
_UART_TX_UUID =      "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

def uuid2bytes(uuid):
    if type(uuid) == int:
        return uuid
    uuid = uuid.encode().replace(b'-',b'')
    tmp = binascii.unhexlify(uuid)
    return bytes(reversed(tmp))

class BLEMANAGER(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            print('Creating the BLEMANAGER object')
            cls._instance = super(BLEMANAGER, cls).__new__(cls)
            print("BLEMANAGER: init")
            cls._instance.ble = Bluetooth()
            cls._instance.ble.set_advertisement(name='JEM', service_uuid=uuid2bytes(_UART_SERVICE_UUID))
            cls._instance.ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=cls._instance.connected_callback)
            cls._instance._connected_handlers = []
            # Put any initialization here.
        cls._instance.ble.advertise(True)
        return cls._instance

    def add_connected_callback(self, handler):
        if self._connected_handlers and handler not in self._connected_handlers:
            self._connected_handlers.append(handler)
        else:
            self._connected_handlers.append(handler)

    def connected_callback(self, bt_o):
        print("BLEMANAGER: connected_callback")
        events = bt_o.events()
        if self._connected_handlers:
            for handler in self._connected_handlers:
                handler(events)


class BLEUART:
    def __init__(self, bleman=None, name="BLEUART", service_uuid = None, rx_uuid = None, tx_uuid = None, aux_uuids = []):
        if bleman is None:
            bleman = BLEMANAGER()
            time.sleep(0.2)
        self.bleman = bleman
        nbr_chars = 3 + len(aux_uuids)
        self.service = self.bleman.ble.service(uuid=uuid2bytes(service_uuid), isprimary=True, nbr_chars=nbr_chars)
        self.rx_characteristic = self.service.characteristic(uuid=uuid2bytes(rx_uuid))
        self.rx_callback = self.rx_characteristic.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=self.rx_cb_handler)
        self.tx_characteristic = self.service.characteristic(uuid=uuid2bytes(tx_uuid))
        self.aux_characteristic = None
        self.aux_chars = {}
        for uuid in aux_uuids:
            self.aux_chars[uuid] = self.service.characteristic(uuid=uuid2bytes(uuid))
            self.aux_characteristic = self.aux_chars[uuid]
        self._connected = False
        self._rx_buffer = bytearray()
        self._connect_status_handler = None
        self.bleman.add_connected_callback(self.connected_callback)
        self.name = name
        self.rx_notifiy_callback = None

    def set_connect_handler(self, handler):
        self._connect_status_handler = handler

    def set_rx_notify_callback(self, callback):
        self.rx_notifiy_callback = callback

    def rx_cb_handler(self, chr, data=None):
        events = chr.events()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            self._rx_buffer += chr.value()
            if self.rx_notifiy_callback:
                self.rx_notifiy_callback()

    def connected_callback(self, events):
        if  events & Bluetooth.CLIENT_CONNECTED:
            self._connected = True
            print("ble_uart_peripheral (%s) connected" % self.name)
            if self._connect_status_handler:
                self._connect_status_handler(self._connected)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            self._connected = False
            print("ble_uart_peripheral (%s) diconnected" % self.name)
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

    def is_connected(self):
        return self._connected
