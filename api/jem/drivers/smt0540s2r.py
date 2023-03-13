# smt0540s2r.py
# buzzer code for PN: SMT-0540-S-2-R
from machine import PWM, Pin

"""
ex:
>> from drivers.smt0540s2r import SMT0540S2R
>> buzz = SMT0540S2R()
>> buzz.start(freq_hz=100)
>> buzz.stop()
>> buff.pwm.duty(100) # 0 - 1024, so 100 = 100/1024 = 10% (about)
"""
class SMT0540S2R:
    DUTY_CYCLE = 512 # don't change this!, 0 - 1024, 512 = 50% duty
    # default esp32 jem-2 IO32
    def __init__(self, sig_pin=32, freq_hz = 400):
        self.sig_pin = sig_pin
        self.freq_hz = freq_hz
        self.pwm = PWM(Pin(sig_pin), freq=500, duty=0)

    def start(self, freq_hz=100):
        self.pwm.duty(SMT0540S2R.DUTY_CYCLE)
        self.pwm.freq(freq_hz)

    def stop(self):
        self.pwm.duty(0)
