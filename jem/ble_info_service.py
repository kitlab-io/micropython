
import struct
from ble_uart_peripheral import IRQ_GATTS_WRITE

class BLEINFOService:
    # service that contains mtu, jem version and other useful hw info
    def __init__(self, jem_ble, service_uuid, rxbuf=2, primary=False):
        self.ble = jem_ble # jem ble wrapper
        self.service = self.ble.service(name="info", uuid=service_uuid, isPrimary=primary)
        # mtu char can be used to tell client what mtu we agreed to
        self.mtu_char = self.service.characteristic(uuid=0x1234, buf_size=rxbuf)
        self.mtu_char.callback(None, self.mtu_cbk)
        self._rx_buffer = bytearray()

    def mtu_cbk(self, chr):
        print("mtu_char_cbk")
        try:
            if IRQ_GATTS_WRITE == chr.event():
                mtu_size = self.ble.get_mtu()
                data = struct.pack("<h", mtu_size)
                self.ble.write(self.mtu_char, data)
        except Exception as e:
            print("mtu_cbk failed %s" % e)

    def notify_mtu(self, connected):
        print("notify_mtu ignore")
