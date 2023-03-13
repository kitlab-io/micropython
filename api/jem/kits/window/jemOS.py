# global listen_button
# global count_button_press
# global is_button_pressed
class JemOS:

    def __init__(self):
        self.listen_button = True
        self.count_button_press = 0
        self.is_button_pressed = False
        self.sleep_input = 500
        self.modes = [
            # None,
            "scrollText",
            "rainbowCycle",
            "theaterChaseRainbow",
        ]
        self.current_mode = 0
        self.exit_current_mode = False


    def on_button_pressed(self, thread_id, **kwargs):
        print("on_button_pressed")
        print(thread_id)
        print(**kwargs)

        if thread_id == "listen_button":
            self.cycle_mode()


    def cycle_mode(self):
        self.current_mode += 1
        if self.current_mode >= len(self.modes):
            self.current_mode = 0

        print(self.current_mode)
        self.activate_mode(self.modes[self.current_mode])


    def activate_mode(self, mode):
        print("activate_mode: " + mode)
        self.exit_current_mode = True
        utime.sleep_ms(300) # wait for current mode to exit

        self.exit_current_mode = False

        # run_play_song()


        if mode == "rainbowCycle":
            # run_rainbowCycle()
            pass
        elif mode == "theaterChaseRainbow":
            # run_theather_chase_rainbow()
            pass
        elif mode == "scrollText":
            # run_scroll_text()
            pass