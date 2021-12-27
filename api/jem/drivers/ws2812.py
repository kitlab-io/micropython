# ws2812.py
# rgb led driver for RGB LED PN ws2812 / neopixel
# Note: this is not used by the JEM pycom chip to control rgbled, that's done in c code
#       this can be used to control JEM rgbled, but also for external rgb leds

# Based on https://github.com/JanBednarik/micropython-ws2812
# Adapted for LoPy by @aureleq, lopy4 updates by Stephen Haynes
# Adapted for JEM WiPy only by @jbthompson.eng@gmail.com

import gc
from machine import SPI
from machine import Pin
from machine import disable_irq
from machine import enable_irq
from uos import uname

class WS2812:
    # Values to put inside SPI register for each color's bit
    buf_bytes = (b'\xE0\xE0', # 0  0b00
                 b'\xE0\xFC', # 1  0b01
                 b'\xFC\xE0', # 2  0b10
                 b'\xFC\xFC') # 3  0b11

    def __init__(self, num_leds=1, brightness=100, data_pin='P11'):
        self.num_leds = num_leds
        self.brightness = brightness

        # Prepare SPI data buffer (8 bytes for each color)
        self.buf_length = self.num_leds * 3 * 8
        self.buf = bytearray(self.buf_length)
        self.data_pin = data_pin # WARNING: only support P11 right now!
        if data_pin != "P11":
            raise Exception("WS2812 does not support data_pin %s" % data_pin)

        # SPI init
        # Bus 0, 8MHz => 125 ns by bit, 8 clock cycle when bit transfert+2 clock cycle between each transfert
        # => 125*10=1.25 us required by WS2812
        self.spi = SPI(0, SPI.MASTER, baudrate=8000000, polarity=0, phase=1)
        # Enable pull down
        # Pin('P11', mode=Pin.OUT, pull=Pin.PULL_DOWN)
        # Turn LEDs off
        self.show([])

    def show(self, data):
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        disable_irq()
        self.spi.write(self.buf)
        enable_irq()
        gc.collect()

    def put_pixel(self, addr, red, green, blue):
        c = (red, green, blue)
        self.update_buf(c, start=addr)

    def update_buf(self, data, start=0):
        buf = self.buf
        buf_bytes = self.buf_bytes
        brightness = self.brightness

        index = start * 24
        for red, green, blue in data:
            red = int(red * brightness // 100)
            green = int(green * brightness // 100)
            blue = int(blue * brightness // 100)

            buf[index:index+2] = buf_bytes[green >> 6 & 0b11]
            buf[index+2:index+4] = buf_bytes[green >> 4 & 0b11]
            buf[index+4:index+6] = buf_bytes[green >> 2 & 0b11]
            buf[index+6:index+8] = buf_bytes[green & 0b11]

            buf[index+8:index+10] = buf_bytes[red >> 6 & 0b11]
            buf[index+10:index+12] = buf_bytes[red >> 4 & 0b11]
            buf[index+12:index+14] = buf_bytes[red >> 2 & 0b11]
            buf[index+14:index+16] = buf_bytes[red & 0b11]

            buf[index+16:index+18] = buf_bytes[blue >> 6 & 0b11]
            buf[index+18:index+20] = buf_bytes[blue >> 4 & 0b11]
            buf[index+20:index+22] = buf_bytes[blue >> 2 & 0b11]
            buf[index+22:index+24] = buf_bytes[blue & 0b11]

            index += 24

        return index // 24

    def fill_buf(self, data):
        end = self.update_buf(data)

        # Turn off the rest of the LEDs
        buf = self.buf
        off = self.buf_bytes[0]
        for index in range(end * 24, self.buf_length):
            buf[index:index+2] = off
            index += 2

    def set_brightness(self, brightness):
        self.brightness = brightness


    def clear(self):
		# turn off the rest of the LEDs
		buf = self.buf
		off = self.buf_bytes[0]
		for index in range(self.buf_length):
			buf[index] = off
			index += 1
