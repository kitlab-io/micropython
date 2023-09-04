# kit.py
# Each kit must provide kit.py
# main.py will look from kits/kit.py in order to run kit
from kits.demo import demo as kit
import _thread

class Kit:
    def __init__(self):
        self._kit = kit

    def start(self):
        self._kit.running = True
        _thread.start_new_thread(self._kit.run, ())

    def stop(self):
        # this should stop the window.run method
        self._kit.running = False
