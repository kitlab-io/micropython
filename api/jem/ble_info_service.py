
import struct


class BLEINFOService:
    # service that contains mtu, jem version and other useful hw info
    def __init__(self, jem_ble, service_uuid, rxbuf=2, primary=False):
        self.ble = jem_ble # jem ble wrapper
        self.service = self.ble.service(uuid=service_uuid, isPrimary=primary)
        # mtu char can be used to tell client what mtu we agreed to
        self.mtu_char = self.service.characteristic(uuid=0x1234, buf_size=rx_buf)
        self.mtu_char.callback(None, self.mtu_cbk)
        self._rx_buffer = bytearray()

    def mtu_cbk(self):
        print("mtu_char_cbk")
        try:
            if IRQ_GATTS_READ == chr.event():
                mtu_size = self.ble.get_mtu()
                data = struct.pack("<h", mtu_size)
                self.ble.write(self.mtu_char, data)
        except Exception as e:
            print("mtu_cbk failed %s" % e)

    def notify_mtu(self):
        print("notify_mtu")
        try:
            mtu_size = self.ble.get_mtu()
            print("mtu_size %s" % mtu_size)
            data = struct.pack("<h", mtu_size)
            self.ble.write(self.mtu_char, data)
        except Exception as e:
            print("notify_mtu failed %s" % e)
