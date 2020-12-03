# JEM micropython api
Micropython code for Jem

## Install
### Required
- JEM Board with Battery or Micro USB Cable
- Computer
- Install [Atom IDE](https://atom.io/)
   + Install [Pymakr plugin](https://atom.io/packages/pymakr) 
### Update JEM Board with latest JEM micropython
- Clone Jem micropython repo
- Plug in battery OR Micro USB Cable
- Press JEM power button for 1 sec and make sure RGB LED flashing every 4 sec or so
- Open Atom IDE and make sure Pymakr plugin installed
- Activate Pymakr plugin so you can see the Terminal at bottom of IDE
- Open Jem Micropython directory micropython/jem/ with Atom
- If using USB
   + Click 'Connect' in Pymakr terminal and select suggested serial port
- If no USB, make sure JEM is on and go to your WiFi settings and connect to the JEM board (wlanxxxx)
   + Then Click 'Connect' in Pymakr terminal and select the WiFi ip address provided
- Make sure pycom firmware version is one of the version we support (Supported Pycom Firmware)
- Click 'Upload' to upload latest JEM micropython to board

### BLE REPL Test
- Turn on JEM with power button (Blue LED should be flashing)
- Visit the Online [Micropython Bluetooth REPL](https://glennrub.github.io/webbluetooth/micropython/repl/)
- Click the 'CONNECT' button and then click on the 'JEM' device
- Now click on the terminal and press enter a couple times and you should see JEM respond with '>>>'
- You can enable or disable the Blue LED as an example
```python
>>>from pycom import heartbeat
>>>hearbeat(False) #verify this disables LED
>>>heartbeat(True) #verify this enabled the flashing LED again
```
- That's it!

### Pycom Firmware Upgrade Instructions
- Only upgrade if firmware on Pycom is not version we support 
#### Supported Pycom Firmware
- Currently we only support Pycom WiPy2.0 with Firmware:
   + WiPy-1.18.2.r7.tar.gz
   + WiPy-1.18.2.r6.tar.gz
   + WiPy-1.18.2.r5.tar.gz
- Do not use latest Pycom firmware as there are known Bluetooth issues

#### Using micro usb cable
- To upgrade the JEM Pycom WiPy MCU with the latest firmware follow instructions here
   + https://docs.pycom.io/gettingstarted/installation/firmwaretool.html
   + Make sure you have a micro usb cable to upgrade with
   + For JEM, connect jumper wires between LED_IN pin and GND and then reset board to force JEM into bootloader mode
      + If you don't do this before running the Pycom firmware upgrade application JEM won't upgrade
   + Make sure to use the legacy firmware mentioned above and not the firmware Pycom automatically assignes 
