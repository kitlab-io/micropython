import _thread
import time
from jem import Jem

_jem = Jem()

from drivers.neopixel import *

# setup neopixel driver to 8x8 LED display
_neopixel = Neopixel()
brightness = 1.0
_neopixel.chain.set_brightness(brightness)

DEFAULT_WAIT_MS = 10

# signals = {
#        exit: exit_current_mode
#    }

class Signals:
    def __init__(self):
        self.exit = False


class WindowKit:
    def __init__(self):
        self.switch_current_window_mode = False
        self.input_debounce_threshold = 0.3
        self.is_button_pressed = False

        self.current_mode = None
        self.current_mode_index = 0
        # self.exit_current_mode = False


        self.signals = Signals()

        # list of func pointers
        self.display_modes = [
           # None,
           ("scrollText", self.display_scroll_text),
           ("rainbowCycle", self.display_rainbow_cycle),
           ("theaterChaseRainbow", self.display_theater_chase_rainbow)
        ]

# to dynamically create UI elements and call functions from REPL
# https://github.com/kitlab-io/micropython/blob/window-kit-v1.0.0/api/jem/kits/window/window.vue#L128


    def run(self):
       print("window.py run")
       self.listen_for_input()
       self.run_window_kit_modes()
       pass


    def listen_for_input(self):
       print("listen_for_input")
       thread_id = _thread.start_new_thread(self.listen_button, ())
       thread_id = _thread.get_ident()
       print(thread_id)
       pass


    def run_window_kit_modes(self):
       print("run_window_kit_modes")
       thread_id = _thread.start_new_thread(self.activate_window_mode, ())
       thread_id = _thread.get_ident()
       print(thread_id)
       pass


    def listen_button(self):
       print("listen_button")
       while True:
          button_state = _jem.btn.read()
          # print(button_state)
          # 0 = pressed button
          # 1 = NOT pressed button

          if button_state == 0:
                # print("button is down")
                # debounce on button pressed
                if not self.is_button_pressed:
                   self.is_button_pressed = True
                   print("on button DOWN!")
                   # send exit signal to cycle display mode
                   self.signals.exit = True
                   # signal should be received in thread activate_window_mode
                   pass
                   #  jemOS.on_button_pressed("listen_button")
                    # if count_button_press >= 3:
                    #     count_button_press = 0
                    #     listen_button = False
                    #     jemOS.listen_button = False
                # else:
                #     print("button still down")

          else:
             # print("button is up")

             if self.is_button_pressed:
                   self.is_button_pressed = False
                   print("on button UP!")
             # else:
             #     print("button still up")

          # start = time.time() # get current time in sec
          # while(button.on()):
          #    pass
          # elapsed = time.time() - start
          # if(elapsed > some_threshold):
          #    change_display_mode() # set global stop signal

          # while(button.off()): # don't do anything, just wait for button to be on
          #    pass


    def on_button_pressed(self):
       print("on_button_pressed")
       pass


    def display_scroll_text(self):
       print("display_scroll_text")
       text = "Hi, I'm JEM! "
       _neopixel.scroll_text(self.signals, text)
       pass


    def display_rainbow_cycle(self):
       print("display_rainbow_cycle")
       _neopixel.rainbowCycle(self.signals, DEFAULT_WAIT_MS)
       pass


    def display_theater_chase_rainbow(self):
        print("display_theater_chase_rainbow")
        _neopixel.theater_chase_rainbow(self.signals, DEFAULT_WAIT_MS)
        pass


    def activate_window_mode(self):
       print("activate_window_mode")
       while True:
          self.current_mode = self.display_modes[self.current_mode_index][1]
          # display mode is a blocking function, running the neopixel drive function
          done = self.current_mode() # neopixel rainbow (ex) will stop once signal says so
          self.signals.exit = False
          # display mode has exited because of stop signal

          # get next display mode
          self.current_mode_index += 1

          # reset counter
          if self.current_mode_index >= len(self.display_modes):
                self.current_mode_index = 0
