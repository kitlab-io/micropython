"""jem.py
Interface used to interact with the JEM hardware:
- Sensors (IMU, light, distance, pressure, temperature...etc)
- GPIO, PWM, I2C, SPI, UART...etc
- RGB LED

Example:
    >> python jem.py
    >> led1 = jem.leds[0]
    >> led1.on = True
    >> led1.red = 200
    >> led1.blue = 100
    >> led1.green = 0
    >> imu = jem.imu
    >> imu.accel.x
    >> 981.0
    >> range = jem.range
    >> range.distance
    >> 56

    >>pio = JemGPIO(1)
    >>pio.mode
    >>'out'
    >>pio.mode='in'
    >>pio.value
    >>0

    >>spi = JemSPI(1)
    >>spi.read(2)
    >>[0x99, 0x01]

    >>i2c = JemI2C(address=0x40)
    >>i2c.read(2)
    >>[0x04, 0x05]

"""
import jembattery
import jembarometer
import jemimu
import jemlight
import jemrange
import jembuzzer
import jemled
from drivers import button
from drivers import peripherals

class Jem(object):
    def __init__(self):
        self.imu = jemimu.JemIMU()
        self.distance = jemrange.JemRange()
        self.light = jemlight.JemLight()
        self.battery = jembattery.JemBattery()
        self.barometer = jembarometer.JemBarometer()
        self.btn = button.Button()
        self.buzzer = jembuzzer.JemBuzzer()
        self.led = jemled.JemLed()
