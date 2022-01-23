""" kit_main.py
Call the desired kit code here (from main.py) and initialized in load_kit method
"""
from kits.demo.demo import Demo
kit_available = True

def load_kit():
    # load kit code here - see example
    print("load_kit")
    try:
        kit = Demo()
        kit.start()
    except Exception as e:
        print("load_kit failed - %s" % e)
        return None
    return kit
