"""
jembuzzer.py
uses the buzzer pn from drivers
ex:
buzz = JemBuzzer()
buzz.start(freq_hz = 100)
buzz.stop()
"""
from drivers.smt0540s2r import SMT0540S2R
class JemBuzzer(SMT0540S2R):
    def __init__(self, **kwargs):
        super(JemBuzzer, self).__init__(**kwargs)

if __name__ == "__main__":
    import time
    freq_hz = 100
    try:
        buzz = JemBuzzer()
        for i in range(5): # run for 5 seconds
            print("buzz freq (hz): %s" % freq_hz)
            buzz.start(freq_hz)
            time.sleep(1)
            freq_hz += 100 # increase hz by 100
    except Exception as e:
        print("failed: %s" % e)

    buzz.stop() # always make sure to stop or battery runs out FAST
