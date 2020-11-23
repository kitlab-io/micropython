#jemble.py
from network import Bluetooth
import uos
import binascii
import time

def uuid2bytes(uuid):
    uuid = uuid.encode().replace(b'-',b'')
    tmp = binascii.unhexlify(uuid)
    return bytes(reversed(tmp))

class RingBuffer():
    def __init__(self, size):
        self.size = size
        self.buffer = bytearray(size)
        self.rd = 0
        self.wr = 0
        self.full = False

    def available(self):
        if self.full == False and self.wr == self.rd:
            return 0
        elif self.full:
            return self.size
        elif self.wr > self.rd:
            return self.size - self.wr + self.rd
        elif self.rd > self.wr:
            return self.size - self.rd + self.wr
        else:
            return 0

    def read(self, num):
        if self.full == False and self.wr == self.rd:
            return None
        data = bytearray(num)
        temp = self.rd
        for i in range(num):
            if self.wr == self.rd and i != 0:
                self.rd = temp
                return None
            else:
                data[i] = self.buffer[self.rd % self.size]
                self.rd += 1

        self.full = False
        return data

    def write(self, data, num):
        if self.full or num > self.size:
            return 0
        temp = self.wr
        for i in range(num):
            if self.wr == self.rd and i != 0:
                self.wr = temp
                return 0
            else:
                self.buffer[self.wr % self.size] = data[i]
                self.wr += 1

        self.full = (self.rd == self.wr)
        return num

class JemBleUart():
    #https://docs.pycom.io/firmwareapi/pycom/network/bluetooth/gattscharacteristic.html
    def __init__(self, service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E", rx_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E", tx_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E", aux_rx_uuid = None, aux_handler=None):
        self.service_uuid = uuid2bytes(service_uuid)
        self.rx_uuid = uuid2bytes(rx_uuid)
        self.tx_uuid = uuid2bytes(tx_uuid)
        self._bt = Bluetooth()
        self._bt.set_advertisement(name='JEM', service_uuid=self.service_uuid)
        self._bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.connected_callback)
        self._bt.advertise(True)
        self.service = self._bt.service(uuid=self.service_uuid, isprimary=True, nbr_chars=3)
        self.rx_characteristic = self.service.characteristic(uuid=self.rx_uuid)
        self.rx_callback = self.rx_characteristic.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=self.rx_cb_handler)
        self.tx_characteristic = self.service.characteristic(uuid=self.tx_uuid)
        self.rx_buffer = RingBuffer(256)
        self.tx_buffer = RingBuffer(500)
        self.prev_term = None
        self.max_len = 20
        self.aux_rx_uuid = None
        self.aux_rx_characteristic = None
        self.aux_rx_callback = None
        self.tx_sent = 0
        if(aux_rx_uuid != None):
            self.aux_rx_uuid = uuid2bytes(aux_rx_uuid)
            self.aux_rx_characteristic = self.service.characteristic(uuid=self.aux_rx_uuid)
            self.aux_rx_callback = self.aux_rx_characteristic.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=aux_handler)


    def connected_callback(self, bt_o):
        events = bt_o.events()
        if  events & Bluetooth.CLIENT_CONNECTED:
            print("Client connected")
            self.prev_term = uos.dupterm()
            uos.dupterm(self)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            if self.prev_term:
                uos.dupterm(self.prev_term)
            print("Client disconnected")


    def rx_cb_handler(self, chr):
        events = chr.events()
        if  events & Bluetooth.CHAR_WRITE_EVENT:
            self.rx_buffer.write(chr.value(), len(chr.value()))

    def read(self, nbytes=None):
        if nbytes == None:
            nbytes = self.rx_buffer.available()
        if nbytes:
            return self.rx_buffer.read(nbytes)
        return None

    def readinto(self, buf, nbytes=None):
        available = self.rx_buffer.available()
        if not available:
            return None

        if nbytes == None or nbytes > available:
            nbytes = available

        for i in range(nbytes):
            buf[i] = self.rx_buffer.read(1)[0]

        return nbytes

    def write(self, buf):
        data_len = len(buf)
        max_len = 20
        chunks = int(data_len / max_len)
        remaining = data_len % max_len
        start = 0
        self.tx_sent += data_len
        for chunk in range(chunks):
            self.tx_characteristic.value(buf[start : start + max_len])
            start += max_len
            self.tx_sent += max_len
            if self.tx_sent >= 20:
                time.sleep(0.050)
                self.tx_sent = 0

        if remaining != 0:
            self.tx_characteristic.value(buf[start : start + remaining])
            self.tx_sent += remaining
            if self.tx_sent >= 20:
                time.sleep(0.050)
                self.tx_sent = 0



        return data_len
