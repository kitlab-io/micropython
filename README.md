# Micropython for JEM
Micropython code for JEM core

## Quickstart
### Install Atom IDE + Pymakr plugin
- [Atom IDE Download](https://atom.io/)
- [Atom Pymakr Plugin](https://atom.io/packages/pymakr)
   + Used by Atom to talk to JEM Micropython

### Flash latest Kitlab JEM Micropython to board
- Download / unzip latest Kitlab JEM micropython [release](https://github.com/kitlab-io/micropython/releases)
- Open Atom IDE and open directory **./micropython/api/jem**
- Turn on JEM board
- Open Pymakr terminal which will appear at bottom of Atom IDE
- Click 'Connect' to talk to JEM
- Click 'Upload' to flash latest code to JEM

### Run Demo application
- JEM Micropython code comes installed with a simple demo app
- With Pymakr terminal open and connect to JEM, press 'Enter' key several times on the terminal to get REPL prompt
- Execute JEM Demo App using following micropython commands from REPL
```bash
>> demo = jem.Demo()

# 1) Make noise when button pressed
>> demo.start_button_buzzer(freq_hz = 100)
# now just press button
>> demo.start_button_buzzer(freq_hz = 400)
# try again ...

# 2) Make noise with motion
>> demo.start_motion_buzzer(min_freq_hz = 100, max_freq_hz = 500)
# now move JEM fast and slow to make low or high pitch sounds

# 3) Make color with range sensor
>> demo.start_color_range()
# move your hand closely over the sensors window and then slowly move up / down - color led should change
```
- Type help to get more demo options
```bash
>> demo.help()
```

## Advanced
Users can control JEM gpio, pwm, adc, dac, uart and read from sensors

### Simple GPIO test
```python
from machine import Pin

# initialize `21` in gpio mode and make it an output
p_out = Pin('21', mode=Pin.OUT)
p_out.value(1)
p_out.value(0)
p_out.toggle()
p_out(True)
```

- For more examples see [Pycom Micropython API](https://docs.pycom.io/firmwareapi/pycom/machine/)

### JEM Sensors
```python
from jemimu import JemIMU
imu = JemIMU()
imu.orientation

from jembattery import JemBattery
batt = JemBattery()
batt.state_of_charge() # 0 - 100%

from jemrange import JemRange
range = JemRange()
range.distance

from jemlight import JemLight
light = JemLight()
light.intensity()

from jembarometer import JemBarometer
bar = JemBarometer()
bar.read()

from drivers import button
btn = button.Button()
btn.read() # should return 0 or 1 depending if pressed

# add buzzer instructions

# add rgb led instructions
```

## Connect over WiFi
- Open Atom IDE and connect to JEM over Pymakr terminal
- In REPL type
```bash
>> from jemwifi import *
>> wifi = setup_wifi(name="JemWifi") # can use any name you want
```
- Open your Wifi network and look for 'JemWifi' then connect
- Now go back to Atom IDE and click 'Connect'
   + select '192.168.4.1'
   + If you don't see an IP Address option restart Atom
- Now you can talk to JEM over Wifi and don't need USB cable
- To keep this setting after reset, put the following code in main.py
```python
from jemwifi import *
wifi = setup_wifi(name="JemWifi")
```
- Then 'Upload' code to board

## JEM Board
![Image of JEM Board V5.1.0](docs/JEM-V5.1.0-drawing.png)

## Update JEM Pycom WIPY 3.0 firmware
- [pycom firmware update](https://docs.pycom.io/updatefirmware/device/)
  + Make sure to use firmware version specified in the JEM Micropython [Releases](https://github.com/kitlab-io/micropython/releases)
