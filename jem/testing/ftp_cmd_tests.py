from jem.cmd import *

def test_fail_cmd():
    print("test_fail_cmd")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    assert(type(fail_cmd) == FTPFailCmd)
    fail_cmd.execute()
    resp = fail_cmd.resp()
    assert(resp != None)
    print("Validate fail_cmd resp can be parsed back into FAIL_RESP cmd")
    checksum_valid, end_i, ftp_cmd = CmdMsg.extract(resp)
    assert(end_i != None)
    assert(type(ftp_cmd) == FTPFailCmd)
    assert(ftp_cmd.id == Cmd.FAIL_RESP)
    if not checksum_valid:
        print("checksum not valid")
    #assert(ftp_cmd.payload == bytearray("test-fail".encode('utf-8')))
    print("SUCCESS")
    return fail_cmd, ftp_cmd

def test_one_shot():
    print("test_one_shot")
    man = CmdManager()
    print("create fail_cmd raw buffer")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    fail_cmd.execute()
    data = fail_cmd.resp()
    print("insert resp into cmd man update")
    resp = man.update(data)
    assert(resp is not None)
    return resp

def test_code_cmd():
    print("test_code_cmd")
    man = CmdManager()
    print("create cmd raw buffer")
    code_cmd = Cmd.create(Cmd.EXE_CODE, "test-code")
    assert(code_cmd.execute() == True)
    cmd_msg = code_cmd.resp()
    print("insert resp into cmd man update")
    assert(cmd_msg is not None)
    return cmd_msg

def test_by_chunks():
    print("test_by_chunks")
    man = CmdManager()
    print("create fail_cmd raw buffer")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    fail_cmd.execute()
    data = fail_cmd.resp()
    print("insert resp into cmd man update one byte each")
    chunk_size = 5
    for i in range(0, len(data), chunk_size):
        resp = man.update(data[i:i+chunk_size])
    assert(resp is not None)
    return resp

def test_chunks_with_junk_data():
    print("test_chunks_with_junk_data")
    man = CmdManager()
    print("create fail_cmd raw buffer")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    fail_cmd.execute()
    buffer = fail_cmd.resp()
    data = bytearray(b'1234')
    data += buffer
    print("insert resp into cmd man update one byte each")
    chunk_size = 5
    for i in range(0, len(data), chunk_size):
        resp = man.update(data[i:i+chunk_size])
    assert(resp is not None)
    return resp

def test_chunks_with_junk_data_in_middle():
    print("test_chunks_with_junk_data_in_middle")
    man = CmdManager()
    print("create fail_cmd raw buffer")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    fail_cmd.execute()
    buffer = fail_cmd.resp()
    data = buffer[0:6]
    data += bytearray(b'123456789abcde')
    print("insert resp into cmd man update one byte each")
    chunk_size = 5
    for i in range(0, len(data), chunk_size):
        resp = man.update(data[i:i+chunk_size])
        if resp is not None:
            break
    assert(resp is not None)
    return resp

def test_junk_data_in_middle_with_good_msg_after():
    print("test_junk_data_in_middle_with_good_msg_after")
    man = CmdManager()
    print("create fail_cmd raw buffer")
    fail_cmd = Cmd.create(Cmd.FAIL_RESP, "test-fail")
    fail_cmd.execute()
    buffer = fail_cmd.resp()
    data = buffer[0:6]
    data += bytearray(b'123456789abcde')

    fail_cmd2 = Cmd.create(Cmd.FAIL_RESP, "test-fail2")
    fail_cmd2.execute()
    buffer2 = fail_cmd2.resp()
    data += buffer2
    print("insert resp into cmd man update using chunks")
    chunk_size = 5
    for i in range(0, len(data), chunk_size):
        resp = man.update(data[i:i+chunk_size])
    assert(resp is not None)
    return resp

def test_write_file_cmd():
    print("test_write_file_cmd")
    file_name = b'test.txt'
    data = b'hello world'
    method = 0 #wb
    pos = 0
    msg = struct.pack("<BLH", method, pos, len(file_name))
    payload = msg + file_name + data
    write_cmd = Cmd.create(Cmd.WRITE_FILE, payload)
    assert(write_cmd.execute() == True)
    return write_cmd

def test_read_file_cmd():
    print("test_read_file_cmd")
    file_name = b'test.txt'
    pos = 0
    rd_len = 5
    msg = struct.pack("<LHH", pos, rd_len, len(file_name))
    payload = msg + file_name
    rd_cmd = Cmd.create(Cmd.READ_FILE, payload)
    assert(rd_cmd.execute() == True)
    print("validate resp")
    resp = rd_cmd.resp()
    checksum_valid, end_i, ftp_cmd = CmdMsg.extract(resp)
    assert(end_i != None)
    assert(type(ftp_cmd) == FTPReadCmd)
    assert(ftp_cmd.id == Cmd.READ_FILE)
    assert(checksum_valid == True)
    return rd_cmd

def test_checksum_file_cmd():
    print("test_checksum_file_cmd")
    file_name = b'test.txt'
    msg = struct.pack("<H", len(file_name))
    payload = msg + file_name
    chk_cmd = Cmd.create(Cmd.FILE_CHECKSUM, payload)
    assert(chk_cmd.execute() == True)
    return chk_cmd

def test_getdir_cmd():
    print("FTPGetDirsCmd test")
    root_name = b'.'
    msg = struct.pack("<H", len(root_name))
    payload = msg + root_name
    cmd = Cmd.create(Cmd.GET_DIRS, payload)
    return cmd
