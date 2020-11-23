"""jemimu.py
Desc: hardware abstraction layer around accel and gyro sensor
Driver used: mpu6050
Example:
    >> imu = JemIMU()
    >> imu.gyro['y'] # deg / sec
    >> 1.3
    >> imu.accel['y'] # g's
    >> 0.983
    >> imu.power_down() # if available, will put device to sleep to save power
    >> imu.pn # part number of driver
    >> "BNO055"
"""

from drivers.bno055 import BNO055
from helpers.helpers import Struct


class JemIMU(BNO055):
    def __init__(self, **kwargs):
        """Initialize JemDevice parent class and then set the comm and mpu6050 driver objects"""
        super(JemIMU, self).__init__(**kwargs)

    @property
    def mag(self):
        """Return mag struct that can reference x, y and z values
        Ex: >> imu = JemIMU()
            >> imu.mag['x']
            >> 0.1
        """
        try:
            mag_data = self.read_magnetometer()
            # get struct so user can access: mag['x']   mag['y']   mag['z']
            mag_struct = Struct(x=mag_data[0], y=mag_data[1], z=mag_data[2])
            return mag_struct
        except Exception as e:
            print("Failed to get mag data from {0} device - {1}".format(self.pn, e))

    @property
    def gyro(self):
        """Return gyro struct that can reference x, y and z values
        Ex: >> imu = JemIMU()
            >> imu.gyro['x']
            >> 0.42
        """
        try:
            gyro_data = self.read_gyroscope()
            # get struct so user can access: gyro['x']   gyro['y']   gyro['z']
            gyro_struct = Struct(x=gyro_data[0], y=gyro_data[1], z=gyro_data[2])
            return gyro_struct
        except Exception as e:
            print("Failed to get gyro from {0} device - {1}".format(self.pn, e))

    @property
    def accel(self):
        """Return accel struct that can reference x, y and z values
        Ex: >> imu = JemIMU()
            >> imu.accel['x']
            >> 1.23
        """
        try:
            accel_data = self.read_accelerometer()
            accel_struct = Struct(x=accel_data[0], y=accel_data[1], z=accel_data[2])
            return accel_struct
        except Exception as e:
            print("Failed to get accel data from {0} device - {1}".format(self.pn, e))


    @property
    def orientation(self):
        """Return roll, pitch, yaw (heading) in degrees
        Ex: >> imu = JemIMU()
            >> imu.orientation['roll']
            >> 34.5
        """
        try:
            orientation_data = self.read_euler()
            orientation_struct = Struct(heading=orientation_data[0], roll=orientation_data[1], pitch=orientation_data[2])
            return orientation_struct
        except Exception as e:
            print("Failed to get orientation data from {0} device - {1}".format(self.pn, e))
