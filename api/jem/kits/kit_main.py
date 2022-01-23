""" kit_main.py
Call the desired kit code here (from main.py) and initialized in load_kit method
"""
from kits.demo.demo import Demo
kit_available = True
kit_running = False
def load_kit(**kwargs):
    global kit_running
    # load kit code here - see example
    print("load_kit")
    try:
        kit = Demo(rc_ble_service=kwargs['rc'])
        kit.start()
        kit_running = True
    except Exception as e:
        print("load_kit failed - %s" % e)
        return None
    return kit
