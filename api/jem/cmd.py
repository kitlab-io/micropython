import struct
import os, sys, json
# FTP helpers used to parse incoming BLE UART FTP Commands for File i/o

OS_IS_DIR_NUM  = 0x4000
def path_join(p1, p2):
    return p1.rstrip("/") + "/" + p2.lstrip("/")

def get_dir_tree(root, tree):
    for f in os.listdir(root):
        path = path_join(root,f)
        is_dir = (os.stat(path)[0] == 0x4000)
        ftype = 'tree' if is_dir else 'blob'
        tree.append({'path': path, 'type': ftype})
        if is_dir:
            get_dir_tree(path, tree)
    return tree

class CmdMsg:
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
        header = CmdMsg.START + struct.pack("<BH",self.id, len(self.payload))
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
        if CmdMsg.START in buffer:

            start_i = 0 # find start of start header index
            for i in range(len(buffer)):
                if CmdMsg.START not in buffer[i:]:
                    break
                else:
                    start_i = i #this is the start index

            if len(buffer[start_i:]) >= (CmdMsg.CMD_ID_I + 1):
                cmd_id = buffer[start_i + CmdMsg.CMD_ID_I]
                if len(buffer[start_i:]) >= (CmdMsg.PAYLOAD_LEN_I + 1):
                    payload_len = struct.unpack("<H",buffer[start_i + CmdMsg.PAYLOAD_LEN_I: start_i + CmdMsg.PAYLOAD_LEN_I + 2])[0]
                    remaining = len(buffer[start_i + CmdMsg.PAYLOAD_I:])
                    if remaining > payload_len:
                        checkum_i = start_i + CmdMsg.PAYLOAD_I + payload_len
                        rx_checksum = buffer[checkum_i]
                        end_i = checkum_i + 1
                        real_checksum = CmdMsg.get_checksum(buffer[start_i: checkum_i])
                        checksum_valid = (rx_checksum == real_checksum)
                        p_start = start_i + CmdMsg.PAYLOAD_I
                        p_end = start_i + CmdMsg.PAYLOAD_I + payload_len
                        if checksum_valid:
                            ftp_cmd = Cmd.create(cmd_id, buffer[p_start: p_end])
                        else:
                            ftp_cmd = Cmd.create(Cmd.FAIL_RESP, "cmd_id %d: checksum failed" % cmd_id)

        return checksum_valid, end_i, ftp_cmd


class Cmd:
    #cmd ids for ftp
    READ_FILE = 3
    WRITE_FILE = 4
    FILE_CHECKSUM = 5
    FAIL_RESP = 6
    #generic cmd ids
    EXE_CODE = 7 # execute some code, used for general cmds not ftp
    #get directory structure
    GET_DIRS = 8
    CMD_ID_LIST = [READ_FILE, WRITE_FILE, FILE_CHECKSUM, FAIL_RESP, EXE_CODE, GET_DIRS]
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
        CMD_ID_MAP = {Cmd.READ_FILE: FTPReadCmd, Cmd.WRITE_FILE: FTPWriteCmd,
        Cmd.FILE_CHECKSUM: FTPChecksumCmd, Cmd.FAIL_RESP: FTPFailCmd, Cmd.EXE_CODE: CodeCmd,
        Cmd.GET_DIRS: FTPGetDirsCmd }

        if id in Cmd.CMD_ID_LIST:
            return CMD_ID_MAP[id](id, payload)
        else:
            print("cmd_id %d, not found, return failed cmd" % id)
            return CMD_ID_MAP[Cmd.FAIL_RESP](Cmd.FAIL_RESP, b"cmd_id invalid")

class FTPFailCmd(Cmd):
    def resp(self):
        return CmdMsg(self.id, self.payload).msg()

class FTPWriteCmd(Cmd):
    FILE_WR_METHOD_I = 0
    FILE_WR_POS_I = FILE_WR_METHOD_I + 1
    FILE_NAME_LEN_I = FILE_WR_POS_I + 4
    METHOD_LIST = ["wb", "ab"]
    def __init__(self, id, payload):
        super().__init__(id, payload)
        self.success = False

    def resp(self):
        msg = b'ok' if self.success else b'fail'
        return CmdMsg(self.id, msg).msg()

    def execute(self):
        method_id = self.payload[FTPWriteCmd.FILE_WR_METHOD_I]
        pos = struct.unpack("<L",self.payload[FTPWriteCmd.FILE_WR_POS_I: FTPWriteCmd.FILE_WR_POS_I + 4])[0]
        fname_len = struct.unpack("<H",self.payload[FTPWriteCmd.FILE_NAME_LEN_I : FTPWriteCmd.FILE_NAME_LEN_I+2])[0]
        fdata_start_i = FTPWriteCmd.FILE_NAME_LEN_I + 2 + fname_len
        fname = self.payload[FTPWriteCmd.FILE_NAME_LEN_I + 2: fdata_start_i].decode('utf-8')
        if (method_id+1) <= len(FTPWriteCmd.METHOD_LIST):
            method = FTPWriteCmd.METHOD_LIST[method_id]
            self.success = self.write(fname, self.payload[fdata_start_i:], pos, method)
        return self.success

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

class CodeCmd(Cmd):
    # just parse some code / raw data for any type of use
    def __init__(self, id, payload):
        super().__init__(id, payload)

    def resp(self):
        return self.payload

    def execute(self):
        return True

class FTPReadCmd(Cmd):
    FILE_RD_POS_I = 0
    FILE_RD_LEN_I = FILE_RD_POS_I + 4
    FILE_NAME_LEN_I = FILE_RD_LEN_I + 2

    def __init__(self, id, payload):
        super().__init__(id, payload)
        self.data = bytearray()

    def resp(self):
        return CmdMsg(self.id, self.data).msg()

    def execute(self):
        pos = struct.unpack("<L",self.payload[FTPReadCmd.FILE_RD_POS_I: FTPReadCmd.FILE_RD_POS_I + 4])[0]
        rd_len = struct.unpack("<H", self.payload[FTPReadCmd.FILE_RD_LEN_I: FTPReadCmd.FILE_RD_LEN_I + 2])[0]
        fname_len = struct.unpack("<H",self.payload[FTPReadCmd.FILE_NAME_LEN_I : FTPReadCmd.FILE_NAME_LEN_I+2])[0]
        fname = self.payload[FTPReadCmd.FILE_NAME_LEN_I + 2: FTPReadCmd.FILE_NAME_LEN_I + 2 + fname_len].decode('utf-8')
        self.data += self.read(fname, pos, rd_len)
        return len(self.data) > 0

    def read(self, name, pos=None, rd_len=None):
        try:
            data = None
            with open(name, "rb") as f:
                if pos is not None:
                    f.seek(pos)
                if rd_len:
                    data = f.read(rd_len)
                else:
                    data = f.read()
        except Exception as e:
            print("Cmd.read failed %s" % e)
        return data

class FTPChecksumCmd(Cmd):
    FILE_LEN_I = 0

    def __init__(self, id, payload):
        super().__init__(id, payload)
        self.checksum = None
        self.file_len = None

    def resp(self):
        msg = struct.pack("<BL", self.checksum, self.file_len)
        return CmdMsg(self.id, msg).msg()

    def execute(self):
        fname_len = struct.unpack("<H",self.payload[FTPChecksumCmd.FILE_LEN_I : FTPChecksumCmd.FILE_LEN_I+2])[0]
        fname = self.payload[FTPChecksumCmd.FILE_LEN_I + 2: FTPChecksumCmd.FILE_LEN_I + 2 + fname_len].decode('utf-8')
        checksum, f_len = self.get_checksum(fname)
        self.checksum = checksum
        self.file_len = f_len
        return self.checksum is not None

    def get_checksum(self, name):
        try:
            c = None
            l = 0
            with open(name, "rb") as f:
                sum = 0
                for line in f.readlines():
                    l += len(line)
                    for d in line:
                        sum = (sum + d) & 0x00FF
                c = ((sum ^ 0xFF) + 1) & 0x00FF
        except Exception as e:
            print("Cmd.get_checksum failed %s" % e)
        return c, l

class FTPGetDirsCmd(Cmd):
    ROOT_NAME_LEN_I = 0

    def __init__(self, id, payload):
        super().__init__(id, payload)
        self.data = ""

    def resp(self):
        return CmdMsg(self.id, self.data).msg()

    def execute(self):
        root_name_len = struct.unpack("<H",self.payload[FTPGetDirsCmd.ROOT_NAME_LEN_I : FTPGetDirsCmd.ROOT_NAME_LEN_I+2])[0]
        root_name = self.payload[FTPGetDirsCmd.ROOT_NAME_LEN_I + 2: FTPGetDirsCmd.ROOT_NAME_LEN_I + 2 + root_name_len].decode('utf-8')
        dir_struct = self.get_dir_list(root_name)
        self.data = json.dumps(dir_struct).encode('utf8') # to raw bytes
        return True

    def get_dir_list(self, root_name):
        # directory structure as list of dictionary elements
        tree = None
        print("get_dir_list root: %s" % root_name)
        try:
            t=[{'path': root_name, 'type':'tree'}]
            tree=get_dir_tree(root=root_name, tree=t)
        except Exception as e:
            print("Cmd.FTPGetDirsCmd failed %s" % e)
        return tree

class CmdManager:
    def __init__(self):
        self.buffer = bytearray()

    def reset(self):
        self.buffer = bytearray()

    def update(self, data):
        self.buffer += data
        checksum_valid, end_index, cmd = CmdMsg.extract(self.buffer)
        if cmd:
            cmd.execute()
            self.buffer = self.buffer[end_index:] #remove old data after parsed
            return cmd.resp()
        return None
