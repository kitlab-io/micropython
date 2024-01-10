# This example demonstrates a peripheral implementing the Nordic UART Service (NUS).

import bluetooth
from ble_advertising import advertising_payload
import utime, json
import struct
import machine, _thread
from micropython import const
import micropython
from machine import Timer

IRQ_CENTRAL_CONNECT = const(1)
IRQ_CENTRAL_DISCONNECT = const(2)
IRQ_GATTS_WRITE = const(3)
IRQ_GATTS_READ_REQUEST = const(4)
IRQ_SCAN_RESULT = const(5)
IRQ_SCAN_DONE = const(6)
IRQ_PERIPHERAL_CONNECT = const(7)
IRQ_PERIPHERAL_DISCONNECT = const(8)
IRQ_GATTC_SERVICE_RESULT = const(9)
IRQ_GATTC_SERVICE_DONE = const(10)
IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
IRQ_GATTC_DESCRIPTOR_DONE = const(14)
IRQ_GATTC_READ_RESULT = const(15)
IRQ_GATTC_READ_DONE = const(16)
IRQ_GATTC_WRITE_DONE = const(17)
IRQ_GATTC_NOTIFY = const(18)
IRQ_GATTC_INDICATE = const(19)
IRQ_GATTS_INDICATE_DONE = const(20)
IRQ_MTU_EXCHANGED = const(21)
IRQ_L2CAP_ACCEPT = const(22)
IRQ_L2CAP_CONNECT = const(23)
IRQ_L2CAP_DISCONNECT = const(24)
IRQ_L2CAP_RECV = const(25)
IRQ_L2CAP_SEND_READY = const(26)
IRQ_CONNECTION_UPDATE = const(27)
IRQ_ENCRYPTION_UPDATE = const(28)
IRQ_GET_SECRET = const(29)
IRQ_SET_SECRET = const(30)

F_READ = bluetooth.FLAG_READ
F_WRITE = bluetooth.FLAG_WRITE
F_NOTIFY = bluetooth.FLAG_NOTIFY
F_READ_WRITE = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE
F_READ_NOTIFY = bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
F_RD_WR_NTFY = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE | bluetooth.FLAG_NOTIFY


_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    F_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    F_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


# Batch writes into ms intervals .
def schedule_in(tmr, handler, delay_ms):
    def _wrap(_arg):
        handler()

    tmr.init(mode=machine.Timer.ONE_SHOT, period=delay_ms, callback=_wrap)



# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)

class BleCharEvent:
    def __init__(self, event, value):
        self.e = event
        self.v = value

    def event(self):
        return self.e

    def value(self):
        return self.v

class BleCharacteristic:
    def __init__(self, name, uuid, buf_size=None):
        self.uuid = bluetooth.UUID(uuid)
        self.handler = None
        self.trigger = None
        self.value_handle = None # this is what we get back from ble after register services / chars
        self.buf_size = buf_size
        self._name = name
        self.buff = bytearray()

    def get_name(self):
        return self._name
      
    def callback(self, trigger, handler):
        # ex: rx_callback = rx_char.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=self.rx_cb_handler)
        self.trigger = trigger
        self.handler = handler

    def irq(self, irq_evt):
        event, value = irq_evt
        self.handler(BleCharEvent(event, value))

class BleService:
    # ex: uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA77"
    DEFAULT_MTU = 23
    def __init__(self, name, uuid, isPrimary=False):
        self.is_primary = isPrimary
        self.uuid = bluetooth.UUID(uuid)
        self.chr_uuids = []
        self.chrs = []
        self._mtu = BleService.DEFAULT_MTU
        self._name = name

    def get_name(self):
        return self._name
      
    def set_mtu(self, mtu_size):
        if mtu_size and (mtu_size >= BleService.DEFAULT_MTU):
            self._mtu = mtu_size

    def get_mtu(self):
        return self._mtu

    def get(self):
        flag = F_RD_WR_NTFY
        chrs = [ [bluetooth.UUID(uuid), flag]  for uuid in self.chr_uuids ]
        service = [ self.uuid, chrs ]
        #ex: service = ( _UART_UUID, (_UART_TX, _UART_RX), )
        return service

    def characteristic(self, uuid, buf_size=None, name="none"):
        if uuid not in self.chr_uuids:
            ble_char = BleCharacteristic(name, uuid, buf_size)
            self.chrs.append(ble_char)
            self.chr_uuids.append(uuid)
            return ble_char
          
    def get_char_by_name(self, name):
        for chr in self.chrs:
            if chr.get_name() == name:
                return chr
        return None

class BLE:
    def __init__(self, esp32_ble, name="JEM-BLE"):
        self._ble = esp32_ble # bluetooth.BLE()
        self.services = []
        self.service_uuids = []
        self.primary_uuid = None
        self.char_handles_map = {}
        self._ble.active(True) # call before gap_name, or name will not change
        self._ble.config(gap_name=name)
        self._ble.config(mtu=256)
        self._ble.irq(self._safe_irq)
        self.tx_delay_ms = 25
        self.tx_chrs = []
        # Increase the size of the rx buffer and enable append mode.
        self._connections = set()
        self._connect_callbacks = []
        self._timer = Timer(0)
        self._timer.init(period=self.tx_delay_ms, callback=self._flush)
        self.errors = []
        self._chr_events = []
        self._running = True
        _thread.stack_size(8*1024)
        self._thrd_id = _thread.start_new_thread(self._chr_handler_thread, ())
        
    def add_connect_callback(self, cbk):
        self._connect_callbacks.append(cbk)

    def connect_callback(self, connected):
        try:
            for cbk in self._connect_callbacks:
                cbk(connected)
        except Exception as e:
            print("connecte_callback: %s" % e)

    def get_mtu(self):
        return self._ble.config('mtu')

    def service(self, name, uuid, isPrimary=False, nbr_chars=0):
        if uuid not in self.service_uuids:
            self.service_uuids.append(uuid)
            service = BleService(name=name, uuid=uuid, isPrimary=isPrimary)
            if isPrimary:
                self.primary_uuid = uuid
            self.services.append(service)
            return service
        else:
            print("oops uuid %d already setup" % uuid)
    
    def get_service_by_name(self, name):
        for sr in self.services:
            if sr.get_name() == name:
                return sr
        return None

    def get_chr_handles(self):
        char_handles = []
        for service in self.services:
            chrs = service.chrs
            char_handles += chrs

        char_handles.reverse() # we reverse so that when we call pop it spits out the as fifo
        return char_handles

    def register(self):
        services = [ service.get() for service in self.services ]
        value_handles = self._ble.gatts_register_services(services)
        # ex: ((self._tx_handle, self._rx_handle), (self._ftp_tx_handle, self._ftp_rx_handle), ) = _ble.gatts_register_services()

        char_handles = self.get_chr_handles()
        # we use the value_handles provided by gatts register ( list of ble characteristic hooks by how they were added by user)
        # to build a connection between the ble characteristic class object we created and the one the esp32 driver created
        self.char_handles_map = {}
        for chr_val_handles in value_handles:
            for value_handle in chr_val_handles:
                char_handle = char_handles.pop()
                self.char_handles_map[value_handle] = char_handle
                # char_handle is instance of BleCharacteristic
                # and value_handle is one created by esp32 ble driver
                char_handle.value_handle = value_handle
                if char_handle.buf_size:
                    self._ble.gatts_set_buffer(char_handle.value_handle, char_handle.buf_size, True)

    def advertising_payload(self):
        services = []
        for service in self.services:
            if service.is_primary:
                services = [ service.uuid ]
                print("adv primary service %s" % service.uuid)

        self._payload = advertising_payload(services=services)
        return self._payload

    def advertise(self, interval_us=500000):
        self.register()
        payload = self.advertising_payload()
        self._ble.gap_advertise(interval_us, adv_data=payload)
	
    def _flush(self, arg):
        try:
            for chr in self.tx_chrs:
                if chr.buff:
                    data = chr.buff[0:100]
                    chr.buff = chr.buff[100:]
                    self._ble.gatts_notify(self.conn_handle, chr.value_handle, data)
        except Exception as e:
            self.errors.append(e)
            print("_flush failed %s" % e)
                  
    def write(self, chr, data):
        # append data to chr buffer and let the _chr_handler_thread take care of the rest
        # _chr_handler_thread is a func run in thread on startup of JEM BLE instance
        try:
            for conn_handle in self._connections:
                self.conn_handle = conn_handle #todo, only set this once
                chr.buff += data
                if chr not in self.tx_chrs:
                    self.tx_chrs.append(chr)

                break # only one connection
        except Exception as e:
          if len(self.errors) <= 50:
              self.errors.append("write %s" % e)

    def close(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)
        self._connections.clear()
    
    def _chr_handler_thread(self):
        self._running = True
        ms = 20
        while self._running:
            chr_evt = None
            utime.sleep_ms(ms)
            if len(self._chr_events):
                chr_evt = self._chr_events[0]
                self._chr_events = self._chr_events[1:len(self._chr_events)]
                ms = 10 # reduce time if something found
                char_handle = chr_evt[0]
                (event, value) = chr_evt[1] # tuple (event, value)
                if event == IRQ_CENTRAL_CONNECT:
                    self.connect_callback(True)
                    print("connected!")
                elif event == IRQ_CENTRAL_DISCONNECT:
                    print("disconnected!")
                    self.connect_callback(False)
                    self.advertise()
                elif event == IRQ_GATTS_WRITE:
                    char_handle.irq((event, value))
                elif event == IRQ_GATTS_READ_REQUEST:
                    char_handle.irq((event, None))
                elif event == IRQ_GATTS_INDICATE_DONE:
                    char_handle.irq((event, None))
            else:
                ms = 20 # set back to default
                
    def _safe_irq(self, event, data):
        try:
            self._irq(event, data)
        except Exception as e:
            print("ble irq failed: %s" % e)
            
    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == IRQ_CENTRAL_CONNECT:
            print("irq event: IRQ_CENTRAL_CONNECT")
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            #self.connect_callback(True)
            self._chr_events.append((None, (event, None)))
        elif event == IRQ_CENTRAL_DISCONNECT:
            print("irq event: IRQ_CENTRAL_DISCONNECT")
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            self._chr_events.append((None, (event, None)))

        elif event == IRQ_GATTS_WRITE or event == IRQ_GATTS_READ_REQUEST or event == IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle = data
            if conn_handle in self._connections and value_handle in self.char_handles_map:
                char_handle = self.char_handles_map[value_handle]  # ex: self.rx_char
                if event == IRQ_GATTS_WRITE:
                    value = self._ble.gatts_read(value_handle)
                    self._chr_events.append((char_handle, (event, value)))
                elif event == IRQ_GATTS_READ_REQUEST:
                    self._chr_events.append((char_handle, (event, None)))
                elif event == IRQ_GATTS_INDICATE_DONE:
                    #char_handle.irq((event, None))
                    self._chr_events.append((char_handle, (event, None)))
            else:
                print("Fail: %s not in %s" % (value_handle, self.char_handles_map))
        elif event == IRQ_GATTC_WRITE_DONE:
            #print("IRQ_GATTC_WRITE_DONE")
            pass

        elif event == IRQ_MTU_EXCHANGED:
            #print("IRQ_MTU_EXCHANGED: %s" % data[1])
            pass

class JEMBLE(object):
    _instance = None
    def __new__(cls, ble_drv=None, name="JEM_BLE"):
        # ble_drv should not be None if this is first time creating jem ble
        if cls._instance is None:
            print('Creating the JEMBLE object')
            cls._instance = super(JEMBLE, cls).__new__(cls)
            print("JEMBLE: init start")
          
            cls._instance.ble = BLE(ble_drv, name=name) #ble drive is esp32 mp ble module, for example
            print("JEMBLE: init done")
        return cls._instance.ble
  
    
class BLEUART:
    def __init__(self, jem_ble, service_uuid, tx_chr_uuid, rx_chr_uuid, rxbuf=100, primary=False, name="uart"):
        self.ble = jem_ble # jem ble wrapper
        self.service = self.ble.service(name, uuid=service_uuid, isPrimary=primary)
        self.tx_char = self.service.characteristic(name="uart_tx", uuid=tx_chr_uuid, buf_size=rxbuf)
        self.rx_char = self.service.characteristic(name="uart_rx", uuid=rx_chr_uuid, buf_size=rxbuf)
        self.rx_char.callback(None, self.rx_cbk)
        self.tx_char.callback(None, self.tx_cbk)

        self._rx_buffer = bytearray()
        self._handler = None

    def rx_cbk(self, chr, data=None):
        try:
            if IRQ_GATTS_WRITE == chr.event():
                value = chr.value()
                self._rx_buffer += value
                if self._handler:
                    self._handler()
        except Exception as e:
            print("rx_cbk failed %s" % e)

    def tx_cbk(self, chr):
        print("tx_char_cbk")

    def irq(self, handler):
        self._handler = handler

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def write(self, data):
        self.ble.write(self.tx_char, data)
