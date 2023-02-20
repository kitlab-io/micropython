from drivers.ws2812 import WS2812
import utime
import uos as os
import pycom

import framebuf

# https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
# https://docs.micropython.org/en/latest/library/neopixel.html?highlight=2812#module-neopixel

#######################################################
### Animation Functions -- edit at your own risk!   ###
### Scroll down for the Main Loop to edit           ###
#######################################################



# wheel: Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.
# Do not change this!

def wheel(wheel_pos):
    wheel_pos = 255 - wheel_pos
    if wheel_pos < 85:
        return (255 - wheel_pos * 3, 0, wheel_pos * 3)
    if wheel_pos < 170:
        wheel_pos -= 85
        return (0, wheel_pos * 3, 255 - wheel_pos * 3)
    wheel_pos -= 170
    return (wheel_pos * 3, 255 - wheel_pos * 3, 0)


pixel_frame_8x8 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

pixel_frame_8x8_catalog = {
    "A":[
        [7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 0, 0, 7, 7, 7],
        [7, 7, 0, 7, 7, 0, 7, 7],
        [7, 7, 0, 7, 7, 0, 7, 7],
        [7, 7, 0, 0, 0, 0, 7, 7],
        [7, 7, 0, 7, 7, 0, 7, 7],
        [7, 7, 0, 7, 7, 0, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7]
    ],
}


def read_framebuf(fbuffer, width, height):
    # FrameBuffer.pixel(x, y[, c])
    # If c is not given, get the color value of the specified pixel.
    # If c is given, set the specified pixel to the given color.

    for y in range(height):
        for x in range(width):
            pixel_color = fbuffer.pixel(x,y)
            print(pixel_color)


def rgb888_to_rgb565(pixel):
    r, g, b = pixel
    # Shift and mask the R, G, and B values to convert to RGB565 format
    r5 = (r * 31 + 127) // 255
    g6 = (g * 63 + 127) // 255
    b5 = (b * 31 + 127) // 255
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    return rgb565

# >>> pixel888 = (255, 128, 64)
# >>> pixel565 = rgb888_to_rgb565(pixel888)
# >>> print(hex(pixel565))
# 0xFD60

def rgb565_to_rgb888(pixel):
    # Extract the R, G, and B components from the RGB565 pixel value
    r5 = (pixel >> 11) & 0x1f
    g6 = (pixel >> 5) & 0x3f
    b5 = pixel & 0x1f
    # Expand the R, G, and B components to 8 bits each
    r8 = (r5 * 255 + 15) // 31
    g8 = (g6 * 255 + 31) // 63
    b8 = (b5 * 255 + 15) // 31
    return (r8, g8, b8)

# >>> pixel565 = 0xFD60
# >>> pixel888 = rgb565_to_rgb888(pixel565)
# >>> print(pixel888)
# (255, 128, 63)


def convert_to_neopixel_frame(fbuffer, width, height, pixels_frame):
    num_pixels = width * height
    # pixels_frame = [(0,0,0)] * num_pixels
    pixel_index = 0

    for y in range(height):
        for x in range(width):
            pixel565 = fbuffer.pixel(x,y)
            pixel888 = rgb565_to_rgb888(pixel565)
            pixels_frame[pixel_index] = pixel888
            pixel_index += 1

    return pixels_frame


class Neopixel:
    DEFAULT_WAIT_MS = 10
    def __init__(self, num_leds=64, brightness=0.05):
        pycom.heartbeat(False) # disable pycom heartbeat for now, might not need to do this
        self.chain = WS2812(num_leds=num_leds, brightness=brightness, data_pin='P11' )
        self.num_leds = num_leds
        self.data = [(0,0,0)] * num_leds

    # scrolling text 8x8 matrix neopixel micropython
    # https://github.com/dsiee/CircuitPython_NeopixelMatrix_Text
    # https://github.com/dborne/scroll_text/blob/main/scroll_text.py
    # https://learn.adafruit.com/adafruit-neopixel-featherwing

    def scroll_text(self, jemOS=None, text="test"):
        print("scroll_text: " + text)
        # classframebuf.FrameBuffer(buffer, width, height, format, stride=width, /)
        # FrameBuffer needs 2 bytes for every RGB565 pixel
        width = 8
        height = 8
        buffer = bytearray(width * height * 2)
        format = framebuf.RGB565
        stride = 8
        fbuf = framebuf.FrameBuffer(buffer, width, height, format, stride)

        pixel888 = (255, 128, 64)
        pixel565 = rgb888_to_rgb565(pixel888)
        print(pixel565)
        print(hex(pixel565))

        fbuf.fill(0)
        # fbuf.text('a', 0, 0, hex(pixel565))
        fbuf.text('a', 0, 0, pixel565)

        # fbuf.hline(0, 8, 1, 0xffff)
        scroll_step = 5
        scroll_wait = 100

        for s in range(scroll_step):
            # read_framebuf(fbuf, width, height)
            # self.data = convert_to_neopixel_frame(fbuf, width, height)
            convert_to_neopixel_frame(fbuf, width, height, self.data)
            self.chain.show( self.data )

            xstep = scroll_step
            ystep = 0
            fbuf.scroll(xstep, ystep)
            # Shift the contents of the FrameBuffer by the given vector.
            # This may leave a footprint of the previous colors in the FrameBuffer.

            utime.sleep_ms(scroll_wait)



        # TODO translate RGB565 to RGB888
        # http://www.fabglib.org/structfabgl_1_1_r_g_b888.html
        # https://github.com/CommanderRedYT/rgb565-converter
        pass




    def write_frame(self):
        self.clear_display()



    # Cycles all the lights through rainbow colors
    def rainbow(self, wait=DEFAULT_WAIT_MS):
        for j in range (0,256,1):
            for i in range (0,self.num_leds,1):
                self.data[i] = wheel((i+j & 255))
            self.chain.show( self.data )
            utime.sleep_ms(wait)

    # Slightly different, this makes the rainbow equally distributed throughout
    def rainbowCycle(self, jemOS=None, wait=DEFAULT_WAIT_MS):
        for j in range (0,256,1):
            for i in range (0,self.num_leds,1):
                self.data[i] = wheel(int((i * 256 / self.num_leds) + j) & 255)
            self.chain.show( self.data )

            if jemOS is not None:
                if jemOS.exit_current_mode == True:
                    return
            utime.sleep_ms(wait)

    # Fill the dots one after the other with a color
    def colorWipe(self, c, wait=DEFAULT_WAIT_MS):
        for i in range(0, self.num_leds, 1):
            self.data[i] = c
            self.chain.show( self.data )
            utime.sleep_ms(wait)

    # Theatre-style crawling lights.
    def theaterChase(self, c, wait=DEFAULT_WAIT_MS):
        for j in range(0, 10, 1):  # do 10 cycles of chasing
            for q in range(0, 3, 1):
                for i in range(0, self.num_leds, 3):
                    try:
                        self.data[i+q] = c # turn every third pixel on
                    except: # if i+q is out of the list then ignore
                        pass
                self.chain.show( self.data )
                utime.sleep_ms(wait)

                for i in range(0, self.num_leds, 3):
                    try:
                        self.data[i+q] = (0,0,0)  # turn every third pixel off
                    except: # if i+q is out of the list then ignore
                        pass

    def theater_chase_rainbow(self, jemOS=None, wait=DEFAULT_WAIT_MS):
        for j in range(0, 256, 1):     # cycle all 256 colors in the wheel
            for q in range(0, 3, 1):
                for i in range(0, self.num_leds, 3):
                    try:
                        self.data[i+q] = wheel((i + j) % 255) #Wheel( int((i+j)) % 255)) # turn every third pixel on
                    except: # if i+q is out of the list then ignore
                        pass
                self.chain.show( self.data )
                if jemOS is not None:
                    if jemOS.exit_current_mode == True:
                        return
                utime.sleep_ms(wait)

                for i in range(0, self.num_leds, 3):
                    try:
                        self.data[i+q] = (0,0,0)  # turn every third pixel off
                    except: # if i+q is out of the list then ignore
                        pass

    # Fill the dots one after the other with a color
    def scroll_wipe(self, wait=DEFAULT_WAIT_MS):
        for j in range(0, 256, 16): # Transition through all colors of the wheel skip every 16 so the change is visible
            for i in range(0, self.num_leds, 1):
                self.data[i] = wheel((j) & 255)
                self.chain.show( data )
                utime.sleep_ms(wait)

    # sparkle the LEDs to the set color or random
    def sparkle(self, c=(127, 127, 127), wait=DEFAULT_WAIT_MS, count=64, random_color=False):
        pixels = [0]*count
        for i in range(len(pixels)):
            pixels[i] = int.from_bytes(os.urandom(1), "big") % self.num_leds
            if random_color:
                c = wheel(int.from_bytes(os.urandom(1), "big")  % 255)
            self.data[pixels[i]] = c
        self.chain.show( self.data )
        utime.sleep_ms(wait)

        for i in range(len(pixels)):
            self.data[pixels[i]] = (0,0,0)

    # Fade the brightness up  down and update a brightness parameter for other modes.
    def fade(self, c=(127, 127, 127), wait=DEFAULT_WAIT_MS):
    # Increases brightness
        for i in range(0, 50, 1):
            self.chain.set_brightness(i)
    # Slows brightness change when dim
            #if i<20:
                #utime.sleep_ms(wait)
    # Updates changes through solid()
            self.solid(c, 0)
        # Decreases Brightness
        for i in range(0, 50, 1):
            i = 50 - i
            self.chain.set_brightness(i)
            #if i<20:
                #utime.sleep_ms(wait)
            self.solid(c, 0)

    # Display a single colour on all LEDs.
    def solid(self, c=(127, 127, 127), wait=DEFAULT_WAIT_MS):
        for i in range(0, self.num_leds, 1):
    # Color set by user variable c and that color's position on the wheel
            self.data[i] = c
        self.chain.show( self.data )
        utime.sleep_ms(wait)


    def set_pixels(self, start_pixel, end_pixel, c=(127,127,127), dir=1):
        for i in range(start_pixel, end_pixel, dir):
            if i >= self.num_leds or i < 0:
                continue
            self.data[i] = c
        self.chain.show( self.data )


    def set_pixel(self, pixel, color):
        #color (r,g,b) = (126,126,45) for example
        if pixel >= self.num_leds or pixel < 0:
            printf("set_pixel %d failed, invalid pixel" % pixel)
        self.data[pixel] = color
        self.chain.show( self.data )

    def clear_display(self):
        #self.chain.clear()
        #self.chain.send_buf()
        for i in range(len(self.data)):
            self.data[i] = (0,0,0)
        self.chain.show(self.data)

    def update_display(self, num_modified_pixels):
        if not num_modified_pixels:
            return
        self.chain.send_buf()

    def put_pixel(self, addr, red, green, blue):
        c = [(red, green, blue)]
        self.chain.update_buf(c, start=addr)
