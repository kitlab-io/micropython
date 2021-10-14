""" kit_main.py
Call the desired kit code here and initialized in load_kit method
jem/main.py will call load kit_main.load_kit  on startup

ex:
def load_kit():
    from drone_kit import DroneKit
    kit = DroneKit()
    kit.start()
    return kit

main.py:
from kits import kit_main
kit = kit_main.load_kit()

"""

class ExampleKit:
    def __init__(self):
        self.name = "ExampleKit"

    def start(self):
        print("ExampleKit started")

    def test_command(self, cmd_id):
        print("ExampleKit received cmd_id %s" % cmd_id)
        return True


def load_kit():
    # load kit code here - see example
    print("load_kit")
    try:
        kit = ExampleKit()
        kit.start()
    except Exception as e:
        print("load_kit failed - %s" % e)
        return None
    return kit
