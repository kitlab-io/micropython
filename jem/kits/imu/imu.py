# imu.py
from jem import jemimu
import time

imu = jemimu.JemIMU()

running = True

def run():
    print("IMU Kit starting")
    start_ms = time.ticks_ms()
    while running:
        try:
            time.sleep_ms(period_ms)
            # angles, example {'roll': -1.75, 'yaw': 359.9375, 'pitch': -5.9375}
            angles = imu.orientation
            accel = imu.accel # ex: {'x':1.9, 'y':5.81, 'z':9.88}

            json_dict = {"angles": angles, "accel": accel}
            json_str = json.dumps(json_dict)
            write(bytes(json_str.encode('utf-8')))
            
            elapsed_ms = time.ticks_ms() - start_ms 
            # send data to kitlab mobile app every 50 millisec
            if elapsed_ms >= 50: 
                start_ms = time.ticks_ms()
        except Exception as e:
            print("imu kit run failed: %s" % e)
            break # make sure to exit !

