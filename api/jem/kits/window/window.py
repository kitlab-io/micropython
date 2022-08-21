# User kit code
# Add your custom code here
# The Mobile app will read this file and generate a button

import json, pycom, time
from kits.window.kit_helper import *
running = True # set this to False to stop the run method below

features = { "buttons": [], "sliders": [] }

# buttons
button = {}
button["func"] = "button_toggle_led"
button["title"] = "Toggle LED"
button["desc"] = "Toggle rgb led"

features["buttons"].append(button)

# slider
slider = {}
slider["func"] = "slider_intensity"
slider["title"] = "intensity"
slider["desc"] = "Set led intensity 1 - 100%"
slider["value"] = 50
slider["min"] = 1
slider["max"] = 100

features["sliders"].append(slider)

features_json = json.dumps(features)
g_led_on = False

# Make a custom button - must include button_somename
def button_toggle_led():
    global g_led_on
    try:
        if g_led_on:
            kit_helper.board.led.set_color(0x000000)
            g_led_on = False
        else:
            kit_helper.board.led.set_color(0x440000)
            g_led_on = True
        return True
    except Exception as e:
        print("button_toggle_led failed: %s" % e)
        return False

# Make custom slider - must include slider_somename
def slider_intensity(value):
    try:
        print("slider_intensity: %s" % value)
        intensity = int(value)
        rgb_val = (intensity/100)*0x440000
        kit_helper.board.led.set_color(int(rgb_val))
    except Exception as e:
        print("feature 2 failed: %s" % e)

# Default behavior - tell kit what to do when not connected to the mobile app

def run():
    global running
    while (kit_helper.connected() == False) and running:
        time.sleep(5)
        print("waiting")
    while kit_helper.connected() and running:
        time.sleep(1) # do whatever here while connected to app
