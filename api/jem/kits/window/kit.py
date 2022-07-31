# User kit code
# Add your custom code here
# The Mobile app will read this file and generate a button for you

import json
features = { "buttons": {}, "sliders": {} }

# pulse button
features["buttons"]["pulse"] = {}
features["buttons"]["pulse"]["func"] = "button_sparkle"
features["buttons"]["pulse"]["title"] = "Sparkle"
features["buttons"]["pulse"]["desc"] = "Create random sparkle"

# slider
features["sliders"]["intensity"] = {}
features["sliders"]["intensity"]["func"] = "slider_intensity"
features["sliders"]["intensity"]["title"] = "intensity"
features["sliders"]["intensity"]["desc"] = "Set led intensity 1 - 100%"
features["sliders"]["intensity"]["min"] = 1
features["sliders"]["intensity"]["max"] = 100

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
