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


    def press_virtual_button(self):
        print('press_virtual_button')
        self._kit.on_button_pressed()
        pass


    def showText(self, text):
        self._kit.display_text = text

        self.run_mode(0) # see window.py self.display_modes
        # # stop the current mode
        # self._kit.auto_cycle_mode = False
        # self._kit.signals.exit = True
        #
        # # switch to mode display text
        # self._kit.current_mode_index = 0
        # self._kit.current_mode = self._kit.display_modes[self._kit.current_mode_index][1]
        # self._kit.signals.exit = False
        # self._kit.current_mode()
        pass


    def run_mode(self, mode_index):
        # stop the current mode
        self._kit.auto_cycle_mode = False
        self._kit.signals.exit = True

        # run target mode
        self._kit.current_mode_index = mode_index
        self._kit.current_mode = self._kit.display_modes[self._kit.current_mode_index][1]
        self._kit.signals.exit = False
        self._kit.current_mode()
        pass


    def showColor(self, color):
        # self._kit.display_solid_color(color)
        self._kit.display_color = color

        self.run_mode(3) # see window.py self.display_modes 
        pass
    

    def off(self):
        self.showColor((0,0,0))