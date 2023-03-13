import _thread
import time
from jem import Jem

_jem = Jem()

switch_current_window_mode = False
input_debounce_threshold = 0.3
is_button_pressed = False




def main():
   print("window.py main")
   listen_for_input()
   run_window_kit_modes()
   pass


def listen_for_input():
   print("listen_for_input")
   thread_id = _thread.start_new_thread(listen_button, ())
   thread_id = _thread.get_ident()
   print(thread_id)
   pass


def run_window_kit_modes():
   print("run_window_kit_modes")
   thread_id = _thread.start_new_thread(activate_window_mode, ())
   thread_id = _thread.get_ident()
   print(thread_id)
   pass


def listen_button():
   print("listen_button")
   while True:
      button_state = _jem.btn.read()
      # print(button_state)
      # 0 = pressed button
      # 1 = NOT pressed button

      if button_state == 0:
            # print("button is down")
            # debounce on button pressed
            if not is_button_pressed:
               is_button_pressed = True
               print("on button DOWN!")
               # send exit signal to cycle display mode
               signals.exit = True
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

         if is_button_pressed:
               is_button_pressed = False
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


def on_button_pressed():
   print("on_button_pressed")
   pass


current_mode = None
current_mode_index = 0
exit_current_mode = False

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

signals = Signals()


def display_scroll_text():
   print("display_scroll_text")
   text = "Hi, I'm JEM! "
   _neopixel.scroll_text, (signals, text)
   pass


def display_rainbow_cycle():
   print("display_rainbow_cycle")
   _neopixel.rainbowCycle, (signals, DEFAULT_WAIT_MS)
   pass


def display_theater_chase_rainbow():
    print("display_theater_chase_rainbow")
    _neopixel.theater_chase_rainbow, (signals, DEFAULT_WAIT_MS)
    pass


# list of func pointers
display_modes = [
   # None,
   ("scrollText", display_scroll_text),
   ("rainbowCycle", display_rainbow_cycle),
   ("theaterChaseRainbow", display_theater_chase_rainbow)
]


def activate_window_mode():
   print("activate_window_mode")
   while True:
      display_mode = display_modes[current_mode][1] 
      # display mode is a blocking function, running the neopixel drive function
      done = display_mode() # neopixel rainbow (ex) will stop once signal says so
      # display mode has exited because of stop signal
      
      # get next display mode
      current_mode += 1

      # reset counter 
      if current_mode >= len(display_modes):
            current_mode = 0 

main()