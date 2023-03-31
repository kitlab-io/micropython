print("jem/boot.py")


# for fastest feedback after power on/reset
import jembuzzer

import time
# from jembuzzer import JemBuzzer

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


def play_note(buzz, note_name, duration_sec=1):
    print("play note: "+note_name)
    frequency = note_freq(note_name)
    # buzz = JemBuzzer()
    buzz.start(frequency)
    time.sleep(duration_sec)
    buzz.stop()
    pass


# notes in scientific pitch notation
# https://en.wikipedia.org/wiki/Scientific_pitch_notation#/media/File:Piano_Frequencies.svg
def play_song(buzz, song_name, beats_per_minute=60):

    melody = [("c4",0.25)]

    # All Ocarina of Time songs
    # https://www.youtube.com/watch?v=cd60Sgob99I
    if song_name == "preludeOfLight":
        # melody = [
        #     ("d5",0.25), ("a4",0.5),
        #     ("d5",0.125), ("a4",0.125), ("b4",0.125), ("d5",0.125)]
        melody = [
            ("d6",0.25), ("a5",0.5),
            ("d6",0.125), ("a5",0.125), ("b5",0.125), ("d6",0.125)
            ]

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
        play_note(buzz, note_name, note_duration)

    pass


def run_play_song():
    buzzer = jembuzzer.JemBuzzer()
    buzz = buzzer
    bpm = 720
    play_song(buzz, "preludeOfLight", 720)
    pass


class Signals:
    def __init__(self):
        self.exit = False

signals = Signals()

from drivers.neopixel import *

import _thread

def startup_feedback():

    run_play_song()

    # buzzer = jembuzzer.JemBuzzer()
    # run_play_song(buzzer)
    # _thread.start_new_thread(run_play_song, ())

    # setup neopixel driver
    _neopixel = Neopixel()
    brightness = 1.0
    _neopixel.chain.set_brightness(brightness)

    # _neopixel.rainbowCycle()
    _thread.start_new_thread(_neopixel.rainbowCycle, (signals, 10))

    pass

# for faster developer iteration
fast_boot = True
# fast_boot = False

if not fast_boot:
    startup_feedback()

    from ble_uart_repl import BLEUARTStream
    from ble_uart_ftp import BLEUARTFTP
    from ble_uart_remote_control import BLEUARTREMOTECONTROL
    rc = BLEUARTREMOTECONTROL()
    ftp = BLEUARTFTP()
    repl = BLEUARTStream()

    signals.exit = True

# NOTE: any imports / variables defined in boot.py should be available in main.py
# the global scope persisted is particular to Micropython
