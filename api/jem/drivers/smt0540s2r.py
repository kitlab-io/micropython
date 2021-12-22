# smt0540s2r.py
# buzzer code for PN: SMT-0540-S-2-R
from machine import PWM

class SMT0540S2R:
    DUTY_CYCLE = 0.5 # don't change this!
    def __init__(self, sig_pin="P7", channel = 0, freq_hz = 400):
        self.sig_pin = sig_pin
        self.freq_hz = freq_hz
        self.channel = channel
        self.pwm = PWM(self.channel, self.freq_hz)
        self.pwm_sig = self.pwm.channel(self.channel, pin=self.sig_pin, duty_cycle=SMT0540S2R.DUTY_CYCLE)

    def start(self, freq_hz=100):
        self.pwm = PWM(self.channel, freq_hz)
        self.pwm_sig.duty_cycle(SMT0540S2R.DUTY_CYCLE)
        self.freq_hz = freq_hz

    def stop(self):
        self.pwm_sig.duty_cycle(0)
