from drivers.ws2812 import WS2812
import utime
import uos as os
import pycom

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

class Neopixel:
    DEFAULT_WAIT_MS = 10
    def __init__(self, num_leds=64, brightness=0.05):
        pycom.heartbeat(False) # disable pycom heartbeat for now, might not need to do this
        self.chain = WS2812(num_leds=num_leds, brightness=brightness, data_pin='P11' )
        self.num_leds = num_leds
        self.data = [(0,0,0)] * num_leds

    # Cycles all the lights through rainbow colors
    def rainbow(self, wait=DEFAULT_WAIT_MS):
        for j in range (0,256,1):
            for i in range (0,self.num_leds,1):
                self.data[i] = wheel((i+j & 255))
            self.chain.show( self.data )
            utime.sleep_ms(wait)

    # Slightly different, this makes the rainbow equally distributed throughout
    def rainbowCycle(self, wait=DEFAULT_WAIT_MS):
        for j in range (0,256,1):
            for i in range (0,self.num_leds,1):
                self.data[i] = wheel(int((i * 256 / self.num_leds) + j) & 255)
            self.chain.show( self.data )
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

    def theater_chase_rainbow(self, wait=DEFAULT_WAIT_MS):
        for j in range(0, 256, 1):     # cycle all 256 colors in the wheel
            for q in range(0, 3, 1):
                for i in range(0, self.num_leds, 3):
                    try:
                        self.data[i+q] = wheel((i + j) % 255) #Wheel( int((i+j)) % 255)) # turn every third pixel on
                    except: # if i+q is out of the list then ignore
                        pass
                self.chain.show( self.data )
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
    def sparkle(self, c=(127, 127, 127), wait=DEFAULT_WAIT_MS, count=2, random_color=False):
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
        self.chain.clear()
        self.chain.send_buf()

    def update_display(self, num_modified_pixels):
        if not num_modified_pixels:
            return
        self.chain.send_buf()

    def put_pixel(self, addr, red, green, blue):
        c = [(red, green, blue)]
        self.chain.update_buf(c, start=addr)
