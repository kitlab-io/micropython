# Kit Remote Control over BLE
from machine import Timer

from ble_uart_peripheral import schedule_in, IRQ_GATTS_WRITE
from cmd import *

class BLEUARTREMOTECONTROL:
    def __init__(self, tmr, uart, sync_uuid = 0xCF33):            
        self._uart = uart
        self._tx_buf = bytearray()
        self.tx_max_len = 100
        self.tx_delay_ms = 20
        self.cmd_delay_ms = 1
        self._uart.irq(self._on_rx)
        self.prev_term = None
        self._cmd_queue = []
        self._timer = tmr
        self.cmd_manager = CmdManager()
        self._exec_cmd = self.schedule_exec_cmd
        
        # add new characteristic to uart service
        self.sync_char = self._uart.service.characteristic(uuid=sync_uuid, buf_size=20)
        self.sync_char.callback(None, self.sync_callback)

    def sync_callback(self, chr, data=None):
        try:
            if IRQ_GATTS_WRITE == chr.event():
                sync_type = chr.value().decode('utf-8').lower()
                if sync_type == 'c':
                    self._cmd_queue.clear()
                if sync_type == 'r':
                    self.cmd_manager.reset()
                if sync_type == 'e':
                    self._exec_cmd = self.schedule_eval_cmd
                if sync_type == 'x':
                    self._exec_cmd = self.schedule_exec_cmd

        except Exception as e:
            print("sync_callback failed: %s" % e)

    def _wrap_flush(self):
        self._flush()
        
    def read(self, sz=None):
        return self._uart.read(sz)

    def _on_rx(self):
        # we got some data!
        try:
            data = self.read()
            code_data = self.cmd_manager.update(data)
            if code_data:
                resp = self.queue_cmd(code_data)
                self.write(resp)
        except Exception as e:
            print("BLEUARTREMOTECONTROL rx_notification failed: %s" % e)

    def queue_cmd(self, data):
        try:
            resp = "ok"
            code = data.decode("utf-8") # convert to string instead of byte array
            self._cmd_queue.append(code)
            self._exec_cmd()
        except Exception as e:
            resp = "queue_cmd failed: %s" % e
            print(resp)
        return resp

    def schedule_eval_cmd(self):
        schedule_in(self._timer, self._wrap_eval_cmd, self.cmd_delay_ms)

    def schedule_exec_cmd(self):
        schedule_in(self._timer, self._wrap_exec_cmd, self.cmd_delay_ms)

    def _wrap_eval_cmd(self, alarm):
        self._execute_next_cmd(eval_cmd=True)

    def _wrap_exec_cmd(self, alarm):
        self._execute_next_cmd(eval_cmd=False)

    def _execute_next_cmd(self, eval_cmd):
        #cmd_handler is called when the RemoteControlBleService receives a valid message from the App over BLE
        try:
            if not self._cmd_queue:
                return
            code = ""
            for code_str in self._cmd_queue:
                code += code_str
            self._cmd_queue.clear()
            if eval_cmd:
                resp = eval(code) # example: eval("move(50,40)") will move car left =50, right=40
                if resp:
                    msg = CmdMsg(Cmd.EXE_CODE, str(resp)).msg()
                    #self.write(bytearray(str(resp)))
                    self.write(msg)
            else:
                exec(code)
        except Exception as e:
            print("_cmd failed: %s" % e)
            self._cmd_queue.clear()
        return

    def _flush(self):
        try:
            data = self._tx_buf[0:self.tx_max_len]
            self._tx_buf = self._tx_buf[self.tx_max_len:]
            self._uart.write(data)
            if self._tx_buf:
                schedule_in(self._timer, self._wrap_flush, self.tx_delay_ms)
        except Exception as e:
            print("_flush failed: %s" % e)

    def write(self, buf):
        empty = not self._tx_buf
        self._tx_buf += buf
        if empty:
            schedule_in(self._timer, self._wrap_flush, self.tx_delay_ms)

    def is_connected(self):
        return self._uart.is_connected()
