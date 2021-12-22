# jembuzzer.py
# uses the buzzer pn from drivers
from drivers.smt0540s2r import SMT0540S2R
class JemBuzzer(SMT0540S2R):
    """
    ex:
    buzz = JemBuzzer()
    buzz.start(freq_hz = 100, duration_sec = 1.0)
    buzz.stop()
    """
    def __init__(self, **kwargs):
        super(JemBuzzer, self).__init__(**kwargs)
