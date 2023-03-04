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

def note_freq(note, octave=4):
    print("note_freq: " + note)
    print(octave)
    # n = "c"
    n = note
    o = octave
    # o = 4 $ default octave
    # n -> c4
    
    # if octave defined with note: "c4" 
    try:
        # try converting to integer
        o = int(note[-1])
        n = note[:-1]
        # n, o = note[:-1], int(note[-1])
    except ValueError:
        pass
    
    index = note_names.index(n)
    return int(round(pow(2, (float(o * 12 + index) / 12.0)) * C0, 2))


def play_note(note_name, duration_sec=1):
    print("play note: "+note_name)
    frequency = note_freq(note_name)
    buzz = JemBuzzer()
    buzz.start(frequency)
    time.sleep(duration_sec)
    buzz.stop()
    pass


# notes in scientific pitch notation
# https://en.wikipedia.org/wiki/Scientific_pitch_notation#/media/File:Piano_Frequencies.svg
def play_song(song_name, beats_per_minute=60):
    
    melody = [("c4",0.25)]
    
    if song_name == "preludeOfLight":
        # melody = [
        #     ("d5",0.25), ("a4",0.5), 
        #     ("d5",0.125), ("a4",0.125), ("b4",0.125), ("d5",0.125)]
        melody = [
            ("d6",0.25), ("a5",0.5), 
            ("d6",0.125), ("a5",0.125), ("b5",0.125), ("d6",0.125)]
    
    # whole note = 1
    # quarter note = 0.25
    # eighth note = 0.125

    # quarter note = 1 beat
    for note in melody:
        note_duration = (60 / beats_per_minute) * (4 * note[1])
        note_name = note[0]
        # note_hz = note_freq(note[0])
        print(note_duration)
        print(note_name)
        play_note(note_name, note_duration)

    pass


def run_play_song():
    play_song("preludeOfLight", 180)
    pass


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


from jemrange import JemRange

# maximum range ~ 14 inches
# distance: 363

# beyond max range
# distance: 8190 || 8191

# minimum distance:
# distance: 30

range_global = [30, 8191]

def get_range_segment(raw_range):

    pass

def run_rangesensor():
    sensor = JemRange()
    # move your hand up / down over the range sensor to see distance change
    for i in range(10): # run for 15 seconds
        print("distance: %s" % sensor.distance)
        time.sleep(1.5)


from jemimu import JemIMU

# orientation guide
# JEM is docked to window kit

# JEM lying down, display down

# USB port FRONT / FACING YOU
# Pixel Display DOWN
# this is the neutral position for IMU (roll 0, yaw 0, pitch 0)
# orientation: {'roll': -3.0, 'yaw': 3.9375, 'pitch': 11.5}



# roll
# rotating around X axis, angle in the Z plane
# 0+ roll rotation upwards from neutral
# 360- roll rotating downwards from neutral
# 0- roll rotating downwards from neutral

# pitch
# rotating around Z axis, angle in the Y plane
# 0+ pitch rotation Counter Clock Wise from neutral
# 360- pitch rotation Clock Wise from neutral

# yaw
# rotating around Y axis, angle in the X plane
# 0+ yaw rotation flat left from neutral
# 360- yaw rotating flat right from neutral

# JEM Window standing up, facing you

# USB port UP
# Pixel Display FRONT / FACING YOU
# orientation: {'roll': -83.125, 'yaw': 0.1875, 'pitch': 121.3125}

# USB port RIGHT
# Pixel Display FRONT / FACING YOU
# orientation: {'roll': 0.5, 'yaw': 248.4375, 'pitch': -86.25}

# USB port LEFT
# Pixel Display FACING YOU
# orientation: {'roll': 0.9375, 'yaw': 97.5, 'pitch': 83.37501}

# USB port DOWN
# Pixel Display FACING YOU
# orientation: {'roll': 87.25, 'yaw': 115.5, 'pitch': 0.1875}


# JEM Window lying down, display up:


# USB port BACK / AWAY FROM YOU
# Pixel Display UP
# orientation: {'roll': 6.9375, 'yaw': 264.8125, 'pitch': -175.1875}


# USB port RIGHT
# Pixel Display UP
# orientation: {'roll': 5.8125, 'yaw': 14.0, 'pitch': 177.5}

# USB port LEFT
# Pixel Display UP
# orientation: {'roll': -3.8125, 'yaw': 172.75, 'pitch': 178.25}

# USB port FRONT / FACING YOU
# Pixel Display UP
# orientation: {'roll': -0.3125, 'yaw': 331.25, 'pitch': 178.5625}


def run_imu():
    imu = JemIMU()
    # move your hand up / down over the range sensor to see distance change
    for i in range(10): # run for 10 seconds
        print("orientation: %s" % imu.orientation)
        time.sleep(1)
    pass


def main():
    setup_neopixel(brightness)
    run_listen_button()

    json_data = read_json_file('kits/window/pixeldata.json')
    print(json_data)

    run_play_song()
    # run_buzzer()

    # run_scroll_text()
    run_rainbowCycle()

    
    # run_rangesensor()
    # run_imu()


main()
