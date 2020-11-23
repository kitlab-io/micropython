"""
smoketest.py
Basic test to verify we can communicate with all the devices on board
"""

from jem import Jem
import utime

class JemSmokeTest:
    def __init__(self):
        self.jem = Jem()

    def test_imu(self):
        print("Capturing initial values")
        ave_roll = 0.0
        ave_pitch = 0.0
        ave_yaw = 0.0
        count = 50
        for i in range(count):
            data = self.jem.imu.orientation
            ave_roll += (data['roll']/count)
            ave_pitch += (data['pitch']/count)
            ave_yaw += (data['heading']/count)
            utime.sleep_ms(10)

        print("Initial values (roll, pitch, yaw): %f, %f, %f" % (ave_roll, ave_pitch, ave_yaw))
        print("Rotate about roll axis at least 20 deg")
        while(abs(self.jem.imu.orientation['roll'] - ave_roll) < 10.0):
            utime.sleep_ms(20)

        print("Roll rotated to %s" % self.jem.imu.orientation['roll'])
        print("Gyro interrupt test, rotate JEM quickly to generate interrupt")
        self.jem.imu.reset_interrupt()
        self.jem.imu.init_gyro_interrupt()
        while self.jem.imu.interrupt_detected() == 0:
            utime.sleep_ms(10)

        print("Interrupt detected, finish")
        self.jem.imu.reset_interrupt()

    def test_barometer(self):
        print("Capturing temperature, pressure and altitude")
        data = self.jem.barometer.read()
        firstTemp = data['temp']
        print("%s" % data)
        print("Change temperature by at least 0.5 deg C")
        temp = self.jem.barometer.read()['temp']
        while abs(temp - firstTemp) < 0.5:
            temp = self.jem.barometer.read()['temp']
            utime.sleep_ms(10)

        print("Temperture changed to %s" % temp)

    def test_range(self):
        print("Capturing current range")
        average = 0
        counts = 50
        for i in range(counts):
            average += self.jem.distance.distance / float(counts)
            print("average = %f" % average)

        print("Current distance value = %s" % average)
        print("Move object over range sensor")
        while(abs(float(self.jem.distance.distance)/average - 1.0) < 0.1):
            utime.sleep_ms(10)

        print("New object detect with range value = %s" % self.jem.distance.distance)

    def test_light(self):
        print("Capturing current light value")
        average = 0
        counts = 50
        for i in range(counts):
            average += self.jem.light.get_analog_value()
        average = average / float(counts)
        print("Current average light value = %s" % average)
        print("Move to to different light source")
        while abs(self.jem.light.get_analog_value() - average) <= 100:
            utime.sleep_ms(10)

        print("New light source detected with value = %s" % self.jem.light.get_analog_value())

    def test_battery(self):
        print("Reading current draw with USB and battery plugged in")
        start_current_ma = self.jem.battery.current_average
        print("start_current_ma = %s" % start_current_ma)
        if(start_current_ma < 0):
            raise Exception("test_battery failed, start_current_ma < 0")
        print("Remove USB, keep battery in")
        while(self.jem.battery.current_average > 0):
            utime.sleep_ms(10)
        print("USB Removed")

    def test_button(self):
        print("Press button")
        while(self.jem.btn.read() == 1):
            utime.sleep_ms(10)
        print("Button press detected!")
