# User kit code
# Add your custom code here
# The Mobile app will read this file and generate a button for you

import json
features = { "buttons": [], "sliders": [] }

# pulse button
button = {}
button["func"] = "button_sparkle"
button["title"] = "Sparkle"
button["desc"] = "Create random sparkle"

features["buttons"].append(button)

# slider
slider = {}
slider["func"] = "slider_intensity"
slider["title"] = "intensity"
slider["desc"] = "Set led intensity 1 - 100%"
slider["min"] = 1
slider["max"] = 100

features["sliders"].append(slider)

features_json = json.dumps(features)

# Make a custom button - must include button_somename
def button_sparkle():
    try:
        kit.neopixel.sparkle(count=10, random_color=False)
        return True
    except Exception as e:
        print("button_sparkle failed: %s" % e)
        return False

# Make custom slider - must include slider_somename
def slider_intensity(value):
    try:
        intensity = int(value)
        kit.neopixel.chain.intensity = intensity/100.0
    except Exception as e:
        print("feature 2 failed: %s" % e)

# Default behavior - tell kit what to do when not connected to the mobile app

def default():
    intensity = 0
    direction = 1
    while kit.connected() == False:
        time.sleep(0.5)
        kit.neopixel.set_intensity(intensity)
        intensity = intensity + (direction * 5);
        if(intensity < 0):
            direction = 1
        if(intensity > 50):
            direction = -1
