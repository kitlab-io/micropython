#main.py
#from kits import kit_main
#kit_main.load_kit()]
from jemwifi import *
from jem_help import jem_help
from jem import Jem

import _thread
import utime

from kits.window.kit_helper import *
helper = KitHelper()

global wlan
# wlan = setup_wifi()

# from kits.kit import Kit

global j
j = Jem()

global np
np = None
global pixel
pixel = 0
global color
color = [100, 0, 0]
global brightness
brightness = 1.0

# kit = Kit()
# kit.start()
# kit.stop()
from drivers.neopixel import *

# setup neopixel driver

def setup_neopixel(_brightness):
    brightness = _brightness
    helper.neopixel.chain.set_brightness(brightness)
    # np = Neopixel(brightness = brightness/100.0)
    # 50 % brightness
    # np.set_pixel(0, (100, 100, 100))
    # return np

# https://docs.micropython.org/en/latest/library/_thread.html
# https://docs.python.org/3.5/library/_thread.html#module-_thread

# _thread.get_ident()
def input_set_pixel():
    pixel = 0
    color = [100, 0, 0]
    run_set_pixel(pixel, color)

# run_set_pixel(2, [0, 100, 0])
def run_set_pixel(pixel, color):
    thread_id = _thread.start_new_thread(helper.neopixel.set_pixel, (pixel, color))
    # helper.neopixel.set_pixel(0, [255, 255, 255])
    print(thread_id)


def run_theather_chase_rainbow():
    DEFAULT_WAIT_MS = 10
    thread_id = _thread.start_new_thread(helper.neopixel.theater_chase_rainbow, (jemOS, DEFAULT_WAIT_MS))
    print(thread_id)
    thread_id = _thread.get_ident()
    print(thread_id)


def run_rainbowCycle():
    DEFAULT_WAIT_MS = 10
    thread_id = _thread.start_new_thread(helper.neopixel.rainbowCycle, (jemOS, DEFAULT_WAIT_MS))
    print(thread_id)
    thread_id = _thread.get_ident()
    print(thread_id)


# def run_sparkle():
#     thread_id = _thread.start_new_thread(helper.neopixel.sparkle, ())
#     # helper.neopixel.sparkle()
#     print(thread_id)
#
#
# def run_theather_chase():
#     c = 2
#     thread_id = _thread.start_new_thread(helper.neopixel.theater_chase, (c))
#     print(thread_id)
#
#
# def run_colorWipe():
#     c = 2
#     thread_id = _thread.start_new_thread(helper.neopixel.colorWipe, (c))
#     print(thread_id)

# global listen_button
# global count_button_press
# global is_button_pressed
class JemOS:

    def __init__(self):
        self.listen_button = True
        self.count_button_press = 0
        self.is_button_pressed = False
        self.sleep_input = 500
        self.modes = [
            # None,
            "scrollText",
            "rainbowCycle",
            "theaterChaseRainbow",
        ]
        self.current_mode = 0
        self.exit_current_mode = False


    def on_button_pressed(self, thread_id, **kwargs):
        print("on_button_pressed")
        print(thread_id)
        print(**kwargs)

        if thread_id == "listen_button":
            self.cycle_mode()


    def cycle_mode(self):
        self.current_mode += 1
        if self.current_mode >= len(self.modes):
            self.current_mode = 0

        print(self.current_mode)
        self.activate_mode(self.modes[self.current_mode])


    def activate_mode(self, mode):
        print("activate_mode: " + mode)
        self.exit_current_mode = True
        utime.sleep_ms(300) # wait for current mode to exit

        self.exit_current_mode = False

        if mode == "rainbowCycle":
            run_rainbowCycle()
        elif mode == "theaterChaseRainbow":
            run_theather_chase_rainbow()
        elif mode == "scrollText":
            run_scroll_text()


listen_button = True
count_button_press = 0
is_button_pressed = False

jemOS = JemOS()


# def listen_button(is_button_pressed, count_button_press):
def listen_button(jemOS, listen_button, is_button_pressed, count_button_press):

    print("start listen_button")
    # listen_button = True
    # count_button_press = 0
    # is_button_pressed = False
    # sleep_input = 500

    # listen_button = jemOS.listen_button
    count_button_press = jemOS.count_button_press
    is_button_pressed = jemOS.is_button_pressed
    sleep_input = jemOS.sleep_input

    # while(listen_button):
    while(jemOS.listen_button):
        # print(jemOS.listen_button)
        # print(listen_button)

        button_state = j.btn.read()
        # print(button_state)
        # 0 = pressed button
        # 1 = NOT pressed button

        if button_state == 0:
            # print("button is down")

            if not is_button_pressed:
                is_button_pressed = True
                print("on button DOWN!")

                jemOS.count_button_press += 1
                print("Button press detected! #"+ str(jemOS.count_button_press))

                kwargs = {
                    "count_button_press": jemOS.count_button_press
                }

                jemOS.on_button_pressed("listen_button")
                # if count_button_press >= 3:
                #     count_button_press = 0
                #     listen_button = False
                #     jemOS.listen_button = False
            # else:
            #     print("button still down")

        else:
            # print("button is up")

            if is_button_pressed:
                is_button_pressed = False
                print("on button UP!")
            # else:
            #     print("button still up")

        utime.sleep_ms(sleep_input)

    print("stop listen_button")


def run_listen_button():
    # thread_id = _thread.start_new_thread(listen_button, (listen_button, is_button_pressed, count_button_press))
    thread_id = _thread.start_new_thread(listen_button, (jemOS, listen_button, is_button_pressed, count_button_press))
    print(thread_id)
    thread_id = _thread.get_ident()
    print(thread_id)


def run_scroll_text():
    # text = "a"
    text = "Hi, I'm JEM! "
    # text = "JEM "
    # helper.neopixel.scroll_text()
    thread_id = _thread.start_new_thread(helper.neopixel.scroll_text, (jemOS, text))
    print(thread_id)
    thread_id = _thread.get_ident()
    print(thread_id)

import time
from jembuzzer import JemBuzzer

# reference for audio helper library
# https://microbit-micropython.readthedocs.io/en/v2-docs/audio.html

# https://github.com/fruch/micropython-buzzer/blob/master/buzzer/__init__.py
# https://github.com/cjbarnes18/micropython-midi

# https://www.cantorsparadise.com/the-mathematical-nature-of-musical-scales-f0a6536bca5d

from math import pow
note_names = ("c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b")

A4 = 440
C0 = A4 * pow(2, -4.75)

def note_freq(note, o=4):
    print("note_freq: " + note)
    # n, o = note[:-1], int(note[-1])
    n = note
    # o = 4
    index = note_names.index(n)
    return int(round(pow(2, (float(o * 12 + index) / 12.0)) * C0, 2))


def run_buzzer():
    freq_hz = 100

    # try:
    #     buzz = JemBuzzer()
    #     for i in range(5): # run for 5 seconds
    #         print("buzz freq (hz): %s" % freq_hz)
    #         buzz.start(freq_hz)
    #         time.sleep(1)
    #         freq_hz += 100 # increase hz by 100
    # except Exception as e:
    #     print("failed: %s" % e)
    #
    # buzz.stop() # always make sure to stop or battery runs out FAST

    buzz = JemBuzzer()
    for n in range(len(note_names)):
        freq_hz = note_freq(note_names[n])
        buzz.start(freq_hz)
        time.sleep(1)

    buzz.stop() # always make sure to stop or battery runs out FAST


    pass

import ujson

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
        json_dict = ujson.loads(data)
        return json_dict


def run_play_pixel_frames():

# green
# 112, 190, 168
# 70BE44
#
# purple
# 137, 80, 159
# 89509F
#
# blue/cyan
# 0, 182, 218
# 00B6DA
#
# magenta
# 232, 21, 128
# E81580
#
# yellow
# 248, 255, 13
# F8E10D
    pass


def load_pixel_frame(frame_data, width=8, height=8):

    color = ()

    for y in range(height):
        for x in range(width):
            px = (y * height) + x

    pass


def main():
    setup_neopixel(brightness)
    run_listen_button()

    json_data = read_json_file('kits/window/pixeldata.json')
    print(json_data)

    # run_scroll_text()
    # text = "JEM "
    # helper.neopixel.scroll_text(jemOS, text)

    run_buzzer()


main()
