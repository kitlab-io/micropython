from jem import jemled, jembuzzer, jemrange, jemlight, jemimu
from jem import jembarometer
from ble_uart_peripheral import JEMBLE
import time, json
import micropython
imu = jemimu.JemIMU() # orientation angles, accel, magnetometer, gyro ..etc
range = jemrange.JemRange() # make distance sensor object
light = jemlight.JemLight() # light sensor
atm = jembarometer.JemBarometer() # atospheric sensor (temp, press, humdity..etc)
ble = JEMBLE() # grab global BLE handler
led = jemled.JemLed()
buzz = jembuzzer.JemBuzzer()
period_ms = 50
# ext_char: a ble characteristic of the remote control ble service
# the ble service that your demo.vue can use to receive kit specific info from JEM
rc_uart = ble.get_service_by_name('rc_uart')
ext_char = rc_uart.get_char_by_name('extra')

color_mode = "none"
global_color = (0,0,0) # rgb

def led_red():
    led.set_color((100, 0, 0))

def led_blue():
    led.set_color((0, 0, 100))

# jem will call the 'run' method in a thread
# put your kit specific behavior here if you want and it will run in background
# try not to use print in the while loop unless it's to print an error

# in repl, you can set running to False to disable the run function below
running = True 

def color_range(hue):
  if hue == 0 or hue > 360:
    return (0,0,0)
  # Ensure hue is in the range [0, 360)
  hue = hue % 360

  # Convert hue to the range [0, 1]
  hue /= 360.0

  # HSV to RGB conversion
  c = 1.0
  x = (1.0 - abs((hue * 6.0) % 2 - 1.0))
  m = 0.0

  if 0 <= hue < 1/6:
      r, g, b = c, x, 0
  elif 1/6 <= hue < 2/6:
      r, g, b = x, c, 0
  elif 2/6 <= hue < 3/6:
      r, g, b = 0, c, x
  elif 3/6 <= hue < 4/6:
      r, g, b = 0, x, c
  elif 4/6 <= hue < 5/6:
      r, g, b = x, 0, c
  else:
      r, g, b = c, 0, x
  scale = 75
  r = int((r + m) * scale)
  g = int((g + m) * scale)
  b = int((b + m) * scale)

  return (r, g, b)

def color_temperature(temp):
    # Map temperature to hue in the range [0, 360)
    if 28 <= temp <= 31:
        hue = ((temp - 28) / 3) * 360
    else:
        hue = 1000  # Default value for other temperatures

    # Pass the hue to the generate_rgb_color function
    return color_range(hue) #(r,g,b)

def color_imu(r, p, y):
    return (abs(int(r)), abs(int(p)), abs(int(y)))
  
def write(data):
    global ext_char
    ble.write(ext_char, data)
    
def run():
    print("Demo Kit starting")
    atm_value = atm.read()
    start_ms = time.ticks_ms()
    while running:
        try:
            update_color = True
            time.sleep_ms(period_ms)
            # angles, example {'roll': -1.75, 'yaw': 359.9375, 'pitch': -5.9375}
            angles = imu.orientation
            json_dict = {"range": range.distance, "light": light.intensity*100, "imu": angles}
            json_dict["atm"] = atm_value#atm.read()
            json_str = json.dumps(json_dict)
            write(bytes(json_str.encode('utf-8')))
            d = range.distance
            if d >= 250:
                d = 0
            d = d*360/250
            if color_mode == "imu":
                c = color_imu(angles['roll'], angles['pitch'], angles['yaw'])
            elif color_mode == "temp":
                c = color_temperature(atm.read()['temp'])
            elif color_mode == "range":
                c = color_range(d)
            elif color_mode == "none" and led.color != global_color:
            	c = global_color
            else:
                update_color = False
            
            if update_color:
                led.set_color(c)
            elapsed_ms = time.ticks_ms() - start_ms 
            if elapsed_ms >= 1000:
                atm_value = atm.read()
                start_ms = time.ticks_ms()
        except Exception as e:
            print("demo kit run failed: %s" % e)
            break # make sure to exit !
