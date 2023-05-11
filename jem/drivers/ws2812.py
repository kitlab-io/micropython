# ws2812.py
# rgb led driver for RGB LED PN ws2812 / neopixel
# Note: this is not used by the JEM pycom chip to control rgbled, that's done in c code
#       this can be used to control JEM rgbled, but also for external rgb leds

# Based on https://github.com/JanBednarik/micropython-ws2812
# Adapted for LoPy by @aureleq, lopy4 updates by Stephen Haynes
# Adapted for JEM WiPy only by @jbthompson.eng@gmail.com

import gc
import machine
import neopixel

class WS2812:
    """
    Driver for WS2812 RGB LEDs. May be used for controlling single LED or chain
    of LEDs.

    Example of use:
        from drivers.ws2812 import *
        chain = WS2812(data_pin=0, num_leds=4)
        data = [
            (255, 0, 0),    # red
            (0, 255, 0),    # green
            (0, 0, 255),    # blue
            (85, 85, 85),   # white
        ]
        chain.show(data)

    Or use raw neopixel driver
    chain = WS2812(spi_data_pin=0, led_count=4)
    np = chain.np
    np[0] = (20, 0, 0)
    np.write() # this will write red to first led
    """
    buf_bytes = (0x88, 0x8e, 0xe8, 0xee)

    def __init__(self, data_pin=0, num_leds=4, brightness=1):
        """
        Params:
        * spi_bus = SPI bus ID (1 or 2)
        * led_count = count of LEDs
        * intensity = light intensity (float up to 1)
        """
        self.led_count = num_leds
        self.intensity = brightness

        # prepare SPI data buffer (4 bytes for each color)
        self.buf_length = self.led_count
        self.np = neopixel.NeoPixel(machine.Pin(data_pin), num_leds)
        # micropython machine neopixel is for controlling ws2812 type rgb led using single wire
        # turn LEDs off
        #self.show([])

    def show(self, data):
        """
        Show RGB data on LEDs. Expected data = [(R, G, B), ...] where R, G and B
        are intensities of colors in range from 0 to 255. One RGB tuple for each
        LED. Count of tuples may be less than count of connected LEDs.
        """
        self.fill_buf(data)
        self.send_buf()

    def send_buf(self):
        """
        Send buffer over neopixel driver bistream / single wire spi like driver
        """
        self.np.write()
        gc.collect()

    def update_buf(self, data, start=0):
        """
        Fill a part of the buffer with RGB data.

        Order of colors in buffer is changed from RGB to GRB because WS2812 LED
        has GRB order of colors. Each color is represented by 4 bytes in buffer
        (1 byte for each 2 bits).

        Returns the index of the first unfilled LED

        Note: If you find this function ugly, it's because speed optimisations
        beated purity of code.
        """

        buf = self.np
        intensity = self.intensity

        mask = 0x03
        index = start * 12
        for red, green, blue in data:
            red = int(red * intensity)
            green = int(green * intensity)
            blue = int(blue * intensity)
            buf[index] = (red, green, blue)

            index += 1

        return index

    def fill_buf(self, data):
        """
        Fill buffer with RGB data.

        All LEDs after the data are turned off.
        """
        end = self.update_buf(data)

        # turn off the rest of the LEDs
        buf = self.np
        for index in range(end, self.buf_length):
            buf[index] = (0,0,0)
            index += 1

    def set_brightness(self, brightness):
        self.intensity = brightness #0.0 - 1.0

    def clear(self):
		# turn off the rest of the LEDs
        buf = self.np
        for index in range(self.buf_length):
            buf[index] = (0,0,0)
            index += 1

        self.send_buf()
