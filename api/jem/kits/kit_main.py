""" kit_main.py
Call the desired kit code here (from main.py) and initialized in load_kit method
"""

kit_available = True
kit_running = False
def load_kit(**kwargs):
    global kit_running
    # load kit code here - see example
    print("load_kit")
    try:
        if 'kit' in kwargs:
            if 'demo' == kwargs['kit'].lower():
                kit = load_demo_kit(**kwargs)
                kit_running = True
            elif 'lantern' == kwargs['kit'].lower():
                kit = load_lantern_kit(**kwargs)
                kit_running = True
        else:
            print("Not kit defined using default Demo")
            kit = load_demo_kit(**kwargs)
    except Exception as e:
        print("load_kit failed - %s" % e)
        return None
    return kit

def load_demo_kit(**kwargs):
    from kits.demo.demo import Demo
    print("load_demo_kit")
    demo = Demo(rc_ble_service=kwargs['rc'])
    demo.start()
    return demo

def load_lantern_kit(**kwargs):
    from kits.lantern.lantern import Lantern
    print("load_lantern_kit")
    lantern_demo = Lantern()
    return lantern_demo
