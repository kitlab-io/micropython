# Proof-of-concept of a FTP over BLE UART.
from machine import Timer
from ble_uart_peripheral import BLEUART
import struct

# BLE UART FTP Service
class FTPCmdResp:
    def __init__(self, data):
        self.data = data

    def resp(self):
        start = FTPCmdParser.CMD_START
        payload_len = struct.pack("<I",len(data))
        checksum = self.get_payload_checksum()
        return start + payload_len + self.data + bytearray([checksum])

    def get_payload_checksum(self):
        sum = 0
        for d in self.data:
            sum = (sum + d) & 0x00FF
        c = ((sum ^ 0xFF) + 1) & 0x00FF
        return c

class FTPCmd:
    # cmd ids
    READ_FILE = 1
    WRITE_FILE = 2
    FILE_CHECKSUM = 3
    FAIL_RESP = 4
    def __init__(self, id, payload):
        self.id = id
        self.payload = payload
        self.success = False

    def execute(self):
        pass

    def resp(self):
        pass

class FTPWriteCmd(FTPCmd):

    def resp(self):
        msg = b'ok' if self.success else b'fail'
        return FTPCmdResp(msg).resp()

    def execute(self):
        fname_len = self.payload[FILE_NAME_LEN_I : FILE_NAME_LEN_I+2]
        fdata_start_i = FILE_NAME_LEN_I + 2 + fname_len
        fname = self.payload[FILE_NAME_LEN_I + 2: fdata_start_i]
        method = self.payload[FILE_WR_METHOD_I]
        pos = self.payload[FILE_WR_POS_I: FILE_WR_POS_I + 4]

        self.success = self.write(fname, self.payload[fdata_start_i:], pos, method)

    def write(self, name, data, pos=None, method="wb"):
        try:
            with open(name, method) as f:
                if pos:
                    f.seek(pos)
                f.write(data)
            return True
        except Exception as e:
            print("FTPWriteCmd.write failed %s" % e)
        return False

class FTPReadCmd(FTPCmd):
    def __init__(self):
        pass

    def read(self, name, pos=None, rd_len=None):
        try:
            data = None
            with open(name, "rb") as f:
                if pos:
                    f.seek(pos)
                data = f.read(rd_len)
        except Exception as e:
            print("FTPCmd.read failed %s" % e)
        return data

class FTPChecksumCmd(FTPCmd):
    def get_checksum(self, name):
        try:
            c = None
            with open(name, "rb") as f:
                sum = 0
                for line in f.readlines():
                    for d in line:
                        sum = (sum + d) & 0x00FF
                c = ((sum ^ 0xFF) + 1) & 0x00FF
        except Exception as e:
            print("FTPCmd.get_checksum failed %s" % e)
        return c

class FTPCmdParser:
    START_STATE = 0
    CMD_ID_STATE = 1
    PAYLOAD_LEN_STATE = 2
    PAYLOAD_STATE = 3
    CHECKSUM_STATE = 4
    CMD_START = bytearray([1,2]) #SOH, STX ascii

    def __init__(self):
        self.state = FTPCmdParser.START
        self.start_index = None
        self.cmd_id = None
        self.payload_len = None
        self.payload = None
        self.checksum = None
        self.checksum_error = None
        self._cmd_id_i = 2
        self._payload_len_i = self._cmd_id_i + 1
        self._payload_i = self._payload_len_i + 2
        self.buffer = bytearray()

    def parse(self, data):
        ftp_cmd = None
        self.buffer += data
        if self.state == FTPCmdParser.START_STATE:
            if FTPCmdParser.CMD_START in self.buffer:
                self.start_i = self.buffer.index(FTPCmdParser.CMD_START)
                self.state = FTPCmdParser.CMD_ID_STATE
        if self.state == FTPCmdParser.CMD_ID_STATE:
            if len(self.buffer[self.start_i:]) >= (self._cmd_id_i + 1) and self.buffer[self.start_i + self._cmd_id_i] in FTPCmdParser.CMD_ID_LIST:
                self.cmd_id = self.buffer[self.start_i + self._cmd_id_i]
                self.state = FTPCmdParser.PAYLOAD_LEN_STATE
        if self.state == FTPCmdParser.PAYLOAD_LEN_STATE:
            if len(self.buffer[self.start_i:]) >= (self._payload_len_i + 1):
                self.payload_len = struct.unpack("<I",self.buffer[self.start_i + self._payload_len_i: self.start_i + self._payload_len_i + 2])[0]
                self.state == FTPCmdParser.PAYLOAD_STATE
        if self.state == FTPCmdParser.PAYLOAD_STATE:
            remaining = len(self.buffer[self.start_i + self._payload_i:])
            if remaining >= self.payload_len:
                self.payload = self.buffer[self.start_i + self._payload_i: self.start_i + self._payload_i + self.payload_len]
                self.state = FTPCmdParser.CHECKSUM_STATE
        if self.state == FTPCmdParser.CHECKSUM_STATE:
            checksum = self.buffer[self.start_i + self._payload_i + self.payload_len]
            calc_checksum = self.get_payload_checksum()
            self.state = FTPCmdParser.START_STATE
            if checksum == calc_checksum:
                ftp_cmd = FTPCmd(self.cmd_id, self.payload)
            else:
                ftp_cmd = FTPCmd(FTPCmd.FAIL_RESP, b"checskum-fail")
                print("FTPCmdParser.parse failed - checksum %d != %d" % (checksum, calc_checksum))
        return ftp_cmd

    def get_payload_checksum(self):
        sum = 0
        start = self.start_i + 2
        end = start + self._payload_i + self.payload_len
        for d in self.buffer[start: end]:
            sum = (sum + d) & 0x00FF
        c = ((sum ^ 0xFF) + 1) & 0x00FF
        return c



class FTPCMDManager:
    CMD_ID_LIST = [FTPCmd.READ_FILE, FTPCmd.WRITE_FILE, FTPCmd.FILE_CHECKSUM]
    def __init__(self):
        self.cmd_parser = FTPCmdParser()

    def update(self, data):
        ftp_cmd = self.ftp_parser.update(data)
        if ftp_cmd:
            ftp_cmd.execute()
            return ftp_cmd.resp()
        return None

class BLEUARTFTP(BLEUART):
    def __init__(self, uart=None):
        if uart is None:
            uart = BLEUART(service_uuid = "6E400001-B5A3-F393-E0A9-E50E24DCCA77", rx_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA77", tx_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA77")
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self._uart.set_connect_handler(self.on_connect_status_changed)
        self.prev_term = None
        self._timer = None
        self._uart.set_rx_notify_callback(self.rx_notification)

    def _wrap_flush(self, alarm):
        self._flush()

    def schedule_tx(self):
        self._timer = Timer.Alarm(self._wrap_flush, ms=self.tx_delay_ms, periodic=False)

    def on_connect_status_changed(self, is_connected):
        if is_connected:
            print("BLEUART_FTP Connected")
        else:
            print("BLEUART_FTP - DISCONNECTED")

    def read(self, sz=None):
        return self._uart.read(sz)

    def rx_notification(self):
        # we got some data!
        data = self.read()
        self.update(data)
        print("rx_notification: %s" % data)

    def update(self, data):
        resp = self.ftp_cmd_manager.update(data)
        if resp:
            self.write(resp)

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
