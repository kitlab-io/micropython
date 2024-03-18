# Kit Remote Control over BLE

from ble_uart_peripheral import schedule_in, IRQ_GATTS_WRITE
from cmd import *


class BLEUARTREMOTECONTROL:
    def __init__(self, tmr, uart, sync_uuid=0xCF33):
        self._uart = uart
        self.cmd_delay_ms = 1
        self._uart.irq(self._on_rx)
        self.prev_term = None
        self._cmd_queue = []
        self._timer = tmr
        self.cmd_manager = CmdManager()

        # add new characteristic to uart service
        self.sync_char = self._uart.service.characteristic(uuid=sync_uuid, buf_size=20)
        self.sync_char.callback(None, self.sync_callback)

        # add new characteristic to uart service
        # extra ble char that user kit can use to asynchronously send data to app
        self.extra_char = self._uart.service.characteristic(name="extra", uuid=0xCD33, buf_size=200)
        self.extra_char.callback(None, self.extra_callback)

    def extra_callback(self, chr, data=None):
        # we use this char to send data to user
        # but if we want to update and use it for both tx and rx then update this callback
        try:
            if IRQ_GATTS_WRITE == chr.event():
                pass
        except Exception as e:
            print("extra_callback failed %s" % e)

    def sync_callback(self, chr, data=None):
        try:
            if IRQ_GATTS_WRITE == chr.event():
                sync_type = chr.value().decode('utf-8').lower()
                if sync_type == 'c':
                    self._cmd_queue.clear()
                if sync_type == 'r':
                    self.cmd_manager.reset()
                if sync_type == 'e':
                    self.schedule_eval_cmd()
                if sync_type == 'x':
                    self.schedule_exec_cmd()

        except Exception as e:
            print("sync_callback failed: %s" % e)

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
            code = data.decode("utf-8")  # convert to string instead of byte array
            self._cmd_queue.append(code)
        except Exception as e:
            resp = "queue_cmd failed: %s" % e
            print(resp)
        return resp

    def schedule_eval_cmd(self):
        schedule_in(self._timer, self._wrap_eval_cmd, self.cmd_delay_ms)

    def schedule_exec_cmd(self):
        schedule_in(self._timer, self._wrap_exec_cmd, self.cmd_delay_ms)

    def _wrap_eval_cmd(self):
        self._execute_next_cmd(eval_cmd=True)

    def _wrap_exec_cmd(self):
        self._execute_next_cmd(eval_cmd=False)

    def _execute_next_cmd(self, eval_cmd):
        # cmd_handler is called when the RemoteControlBleService receives a valid message from the App over BLE
        try:
            if not self._cmd_queue:
                return
            code = ""
            while self._cmd_queue:
                code = self._cmd_queue.pop()
                if eval_cmd:
                    resp = eval(code)  # example: eval("move(50,40)") will move car left =50, right=40
                    msg = CmdMsg(Cmd.EXE_CODE, str(resp)).msg()
                    self.write(msg)
                else:
                    exec(code)
        except Exception as e:
            print("_cmd failed: %s" % e)
            self._cmd_queue.clear()
        return

    def write(self, buf):
        self._uart.write(buf)

    def write_extra(self, buf):
        self._uart.ble.write(self.extra_char, buf)

    def is_connected(self):
        return self._uart.is_connected()
 
