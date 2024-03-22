# imu.py

from jem import jemimu
import time

imu = jemimu.JemIMU()


# Tutorial_1

# create new buzzer based on smt0540s2r driver (see jem/drivers)
buzzer = JemBuzzer()

# define our new function
def buzz():
    # global: you don't have to do this, but it's good practice
    # just let's python know that buzzer object was defined somewhere else
    global buzzer

    # make sound based on the frequency (Hertz) for some time
    buzzer.start(freq_hz)
    time.sleep(0.100)
    buzzer.stop()

# this tells the imu interrupt to call our newly created buzz function each time the imu is moved
imu._int.irq(buzz) 

# Tutorial_1 !

running = True

def run():
    print("IMU Kit starting")
    start_ms = time.ticks_ms()
    while running:
        try:
            time.sleep_ms(period_ms)
            # angles, example {'roll': -1.75, 'yaw': 359.9375, 'pitch': -5.9375}
            angles = imu.orientation
            accel = imu.read_accelerometer()

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


