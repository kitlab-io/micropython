import struct

def test_fail_cmd():
    print("FTPCmd.create(FTPCmd.FAIL_RESP, 'test-fail')")
    fail_cmd = FTPCmd.create(FTPCmd.FAIL_RESP, "test-fail")
    assert(type(fail_cmd) == FTPFailCmd)
    fail_cmd.execute()
    resp = fail_cmd.resp()
    assert(resp != None)
    print("Validate fail_cmd resp can be parsed back into FAIL_RESP cmd")
    checksum_valid, end_i, ftp_cmd = FTPCmdMsg.extract(resp)
    assert(end_i != None)
    assert(type(ftp_cmd) == FTPFailCmd)
    assert(ftp_cmd.id == FTPCmd.FAIL_RESP)
    if not checksum_valid:
        print("checksum not valid")
    #assert(ftp_cmd.payload == bytearray("test-fail".encode('utf-8')))
    print("SUCCESS")
    return fail_cmd, ftp_cmd

# FTP Classes used to parse incoming BLE UART FTP Commands for File i/o
class FTPCmdMsg:
    START = bytearray([1,2]) #SOH, STX ascii
    START_I = 0
    CMD_ID_I = START_I + 2
    PAYLOAD_LEN_I = CMD_ID_I + 1
    PAYLOAD_I = PAYLOAD_LEN_I + 2
    def __init__(self, id, payload):
        self.id = id
        if type(payload) == str:
            self.payload = bytearray(payload.encode('utf-8'))
        elif type(payload) == list:
            self.payload = bytearray(payload)
        else:
            self.payload = payload

    def msg(self):
        header = FTPCmdMsg.START + struct.pack("<BH",self.id, len(self.payload))
        checksum = self.get_checksum(header + self.payload)
        return header + self.payload + bytearray([checksum])

    @staticmethod
    def get_checksum(data):
        sum = 0
        for d in data:
            sum = (sum + d) & 0x00FF
        c = ((sum ^ 0xFF) + 1) & 0x00FF
        return c

    @staticmethod
    def extract(buffer):
        start_i, end_i, cmd_id, payload_len, checksum_valid = None, None, None, None, None
        ftp_cmd = None
        if FTPCmdMsg.START in buffer:
            start_i = buffer.index(FTPCmdMsg.START)
            print("start_i: %d" % start_i)
            if len(buffer[start_i:]) >= (FTPCmdMsg.CMD_ID_I + 1):
                cmd_id = buffer[start_i + FTPCmdMsg.CMD_ID_I]
                print("cmd_id: %d" % cmd_id)
                if len(buffer[start_i:]) >= (FTPCmdMsg.PAYLOAD_LEN_I + 1):
                    payload_len = struct.unpack("<H",buffer[start_i + FTPCmdMsg.PAYLOAD_LEN_I: start_i + FTPCmdMsg.PAYLOAD_LEN_I + 2])[0]
                    print("payload_len: %d" % payload_len)
                    remaining = len(buffer[start_i + FTPCmdMsg.PAYLOAD_I:])
                    if remaining >= payload_len:
                        payload_ready = True
                    if remaining > payload_len:
                        checksum_ready = True
                        checkum_i = start_i + FTPCmdMsg.PAYLOAD_I + payload_len
                        rx_checksum = buffer[checkum_i]
                        end_i = checkum_i + 1
                        real_checksum = FTPCmdMsg.get_checksum(buffer[start_i: checkum_i])
                        print("checkum_i: %d, got: %d, exp: %d" % (checkum_i, rx_checksum, real_checksum))
                        checksum_valid = (rx_checksum == real_checksum)
                        p_start = start_i + FTPCmdMsg.PAYLOAD_I
                        p_end = start_i + FTPCmdMsg.PAYLOAD_I + payload_len
                        if checksum_valid:
                            ftp_cmd = FTPCmd.create(cmd_id, buffer[p_start: p_end])
                        else:
                            ftp_cmd = FTPCmd.create(FTPCmd.FAIL_RESP, "cmd_id %d: checksum failed" % cmd_id)

        return checksum_valid, end_i, ftp_cmd


class FTPCmd:
    #cmd ids
    READ_FILE = 1
    WRITE_FILE = 2
    FILE_CHECKSUM = 3
    FAIL_RESP = 4
    CMD_ID_LIST = [READ_FILE, WRITE_FILE, FILE_CHECKSUM, FAIL_RESP]
    def __init__(self, id, payload):
        self.id = id
        if type(payload) == str:
            self.payload = bytearray(payload.encode('utf-8'))
        elif type(payload) == list:
            self.payload = bytearray(payload)
        else:
            self.payload = payload

    def execute(self):
        pass

    def resp(self):
        pass

    @classmethod
    def create(cls, id, payload):
        CMD_ID_MAP = {FTPCmd.READ_FILE: FTPReadCmd, FTPCmd.WRITE_FILE: FTPWriteCmd, FTPCmd.FILE_CHECKSUM: FTPChecksumCmd, FTPCmd.FAIL_RESP: FTPFailCmd}
        if id in FTPCmd.CMD_ID_LIST:
            return CMD_ID_MAP[id](id, payload)
        return None

class FTPFailCmd(FTPCmd):
    def resp(self):
        return FTPCmdMsg(self.id, self.payload).msg()

class FTPWriteCmd(FTPCmd):
    FILE_WR_METHOD_I = 0
    FILE_WR_POS_I = FILE_WR_METHOD_I + 1
    FILE_NAME_LEN_I = FILE_WR_POS_I + 4

    def __init__(self):
        self.success = False

    def resp(self):
        msg = b'ok' if self.success else b'fail'
        return FTPCmdMsg(self.id, msg).msg()

    def execute(self):
        fname_len = self.payload[FTPWriteCmd.FILE_NAME_LEN_I : FTPWriteCmd.FILE_NAME_LEN_I+2]
        fdata_start_i = FTPWriteCmd.FILE_NAME_LEN_I + 2 + fname_len
        fname = self.payload[FTPWriteCmd.FILE_NAME_LEN_I + 2: fdata_start_i]
        method = self.payload[FTPWriteCmd.FILE_WR_METHOD_I]
        pos = self.payload[FTPWriteCmd.FILE_WR_POS_I: FTPWriteCmd.FILE_WR_POS_I + 4]

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
        self.data = bytearray()

    def resp(self):
        return FTPCmdMsg(self.id, self.data).msg()

    def execute(self):
        rd_len = self.payload[FTPReadCmd.FILE_NAME_LEN_I: FTPReadCmd.FILE_NAME_LEN_I + 2]
        pos = self.payload[FTPWriteCmd.FILE_RD_POS_I: FTPWriteCmd.FILE_RD_POS_I + 4]
        fname_len = self.payload[FTPReadCmd.FILE_NAME_LEN_I : FTPReadCmd.FILE_NAME_LEN_I+2]
        fdata_start_i = FTPReadCmd.FILE_NAME_LEN_I + 2 + fname_len
        fname = self.payload[FTPReadCmd.FILE_NAME_LEN_I + 2: fdata_start_i]
        self.data += self.read(fname, pos, method)


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

class FTPCMDManager:
    def __init__(self):
        self.buffer = bytearray()

    def update(self, data):
        self.buffer += data
        checksum_valid, end_index, ftp_cmd = FTPCmdMsg.extract(self.buffer)
        if ftp_cmd:
            ftp_cmd.execute()
            self.buffer = self.buffer[end_index:] #remove old data after parsed
            return ftp_cmd.resp()
        return None