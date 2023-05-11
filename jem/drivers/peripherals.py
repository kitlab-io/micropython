from machine import I2C, SPI, Pin
from ustruct import unpack as unp
from ustruct import pack


"""JemBoardPins
Key number is the JEM Hardware Pin # shown on enclosure
The first element in the list is the actual MCU pin number
"""
JEM_AVAILABLE_MCU_PINS = {0: ["IO0"]}

JEM_DEFAULT_I2C_BUS = 0
JEM_DEFAULT_I2C_PINS = {'scl':18, 'sda': 19}
JEM_DEFAULT_I2C_BAUDRATE = 40000 #should be 100KHz but i2c clk stretching issues with bq27441, so use 40KHz for now

class JemI2C(object):
    """JemI2C
    Wrapper around micropython I2C class with helper functions
    Warning: older versions of Micropython for the wipy2.0 only have 1 i2c port but newer versions have more
    """
    def __init__(self, i2c, address):
        self.address = address
        self._device = i2c

    def write_raw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self.write(value)
        #print("Wrote 0x%02X",value)

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self.write_reg(register, value)
        #print("Wrote 0x%02X to register 0x%02X", value, register)

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""

        #need to convert to bytearray first
        data = pack('H', value) # convert to unsigned 16 bit bytearray

        self.write_reg(register, data)
        #print("Wrote 0x%04X to register pair 0x%02X, 0x%02X", value, register, register + 1)

    def write_list(self, register, data):
        """Write bytes to the specified register."""
        self.write_reg(register, data)
        #print("Wrote to register 0x%02X: %s", register, data)

    def read_list(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        results = self.read_reg(register, length)
        #print("Read the following from register 0x%02X: %s", register, results)
        return results

    def read_raw8(self):
        """Read an 8-bit value on the bus (without register)."""
        result = self.read(1) # returns bytearray of len 1
        #print("Read 0x%02X",result)

        # convert to dec number
        return ord(result[0])

    def read_u8(self, register):
        """Read an unsigned byte from the specified register."""
        data = self.read_reg(register, 1)
        result = unp('B', data)
        #print("Read 0x%02X from register 0x%02X", result, register)
        return result[0]

    def read_s8(self, register):
        """Read a signed byte from the specified register."""
        data = self.read_reg(register, 1)
        result = unp('b', data)
        return result[0]

    def read_u16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""

        #TODO: need to handle array first
        data = self.read_reg(register, 2)
        #print("Read 0x%04X from register pair 0x%02X, 0x%02X", result, register, register + 1)
        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = unp('<H', data) # convert byte array to unsigned short little endian number
            #result = ((result << 8) & 0xFF00) + (result >> 8)
        else:
            result = unp('>H', data)  # convert byte array to unsigned short big endian number

        return result[0]

    def read_s16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        data = self.read_reg(register, 2)

        if not little_endian:
            result = unp('<h', data)  # convert byte array to signed short little endian number
            # result = ((result << 8) & 0xFF00) + (result >> 8)
        else:
            result = unp('>h', data)  # convert byte array to signed short big endian number

        return result[0]

    def read_u16_le(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        return self.read_u16(register, little_endian=True)

    def read_u16_be(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        return self.read_u16(register, little_endian=False)

    def read_s16_le(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        return self.read_s16(register, little_endian=True)

    def read_s16_be(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        return self.read_s16(register, little_endian=False)

    def get_bytes(self, data):
        """Return data converted to bytearray"""
        #print("JemI2c - get_bytes of type %s" % (type(data)))
        if type(data) == list or type(data) == str or type(data) == bytes:
            data = bytearray(data)

        elif type(data) != bytearray:
            data = bytearray([data])

        #print("JemI2c - get_bytes returned %s" % data)
        return data

    def write_reg(self, reg, data):
        bytes_data = self.get_bytes(data)
        self._device.writeto_mem(self.address, reg, bytes_data)

    def read_reg(self, reg, length):
        """Return length bytes read from register of i2c address"""
        result = self._device.readfrom_mem(self.address, reg, length)
        return result

    def read(self, num_bytes):
        data = self._device.readfrom(self.address, num_bytes)
        return data


    def write(self, data):
        """Write to i2c address and return num bytes successfully written"""
        bytes_data = self.get_bytes(data)
        num_written = self._device.writeto(self.address, bytes_data) # send bytearray to address
        return num_written



class JemSPI(object):
    """JemSPI
    Handler for SPI device communication
    """

    def __init__(self, spi, select_pin, pull=None):
        self._device = spi
        self.select_pin = Pin(select_pin, mode=Pin.OUT, pull=pull)
        self.select_pin.value(1)


    def write(self, data):
        """Write to spi by first pulling select pin, eturn num bytes successfully written"""

        self.select_pin.off() # pull line low to enable communication with spi device
        num_written = self._device.write(data)  # send bytes on the bus
        self.select_pin.on()

        return num_written

    def read(self, num_bytes):
        """Read from spi bus and return bytes read as bytearray"""

        self.select_pin.off() # pull select pin low to enable communication with spi bus
        data = self._device.read(num_bytes)
        self.select_pin.on() # pull select pin back high to disable communinicaion with spi bus

        return data


class JemPin(Pin):
    """Jem wrapper around GPIO Pin class
    Checks if pin requested is already in use or is restricted / used by Jem hardware
    If not then returns a warning
    """
    def __init__(self, *args, **kwargs):
        self.pin = args[0] # pin number is required
        if(self.pin not in JEM_AVAILABLE_MCU_PINS):
            print("Warning: pin %s is used by existing Jem hardware and could interfere with sensors" % self.pin)

        super(JemPin, self).__init__(*args, **kwargs)
