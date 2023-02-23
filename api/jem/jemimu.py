"""jemimu.py
Desc: hardware abstraction layer around accel and gyro sensor
Driver used: BNO055
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

class JemIMU(BNO055):
    def __init__(self, **kwargs):
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
            return {'x':mag_data[0], 'y':mag_data[1], 'z':mag_data[2]}
        except Exception as e:
            print("mag failed - from {0} device - {1}".format(self.pn, e))

    @property
    def gyro(self):
        """Return gyro struct that can reference x, y and z values
        Ex: >> imu = JemIMU()
            >> imu.gyro['x']
            >> 0.42
        """
        try:
            d = self.read_gyroscope()
            # get struct so user can access: gyro['x']   gyro['y']   gyro['z']
            return {'x':d[0], 'y':d[1], 'z':d[2]}
        except Exception as e:
            print("gyro failed - from {0} device - {1}".format(self.pn, e))

    @property
    def accel(self):
        """Return accel struct that can reference x, y and z values
        Ex: >> imu = JemIMU()
            >> imu.accel['x']
            >> 1.23
        """
        try:
            d = self.read_accelerometer()
            return {'x':d[0], 'y':d[1], 'z':d[2]}
        except Exception as e:
            print("accel failed - from {0} device - {1}".format(self.pn, e))


    @property
    def orientation(self):
        """Return roll, pitch, yaw (heading) in degrees
        Ex: >> imu = JemIMU()
            >> imu.orientation['roll']
            >> 34.5
        """
        try:
            d = self.read_euler()
            return {'yaw':d[0], 'roll':d[1], 'pitch':d[2]}
        except Exception as e:
            print("orientation failed - from {0} device - {1}".format(self.pn, e))

if __name__ == "__main__":
    import time
    imu = JemIMU()
    # rotate JEM to see orientation 
    for i in range(10): # run for 10 seconds
        print("orientation: %s" % imu.orientation)
        time.sleep(1)
