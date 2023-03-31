# kit.py
# Each kit must provide kit.py
# main.py will look from kits/kit.py in order to run kit
from kits.window import window
import _thread

class Kit:
    def __init__(self):
        self._kit = window.WindowKit()

    def start(self):
        print("Kit.start")
        self._kit.running = True
        _thread.start_new_thread(self._kit.run, ())

    def stop(self):
        print("Kit.stop")
        # this should stop the window.run method
        self._kit.running = False
