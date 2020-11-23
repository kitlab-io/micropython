# micropython
Micropython code for Jem


## Quickstart guide 
- Currently we only support Pycom WiPy2.0 with Firmware:
   + WiPy-1.18.2.r7.tar.gz
   + WiPy-1.18.2.r6.tar.gz
   + WiPy-1.18.2.r5.tar.gz
- Do not use latest Pycom firmware as there are known Bluetooth issues
   
### Pycom Firmware Upgrade Instructions
#### Using micro usb cable
- To upgrade the JEM Pycom WiPy MCU with the latest firmware follow instructions here
   + https://docs.pycom.io/gettingstarted/installation/firmwaretool.html
   + Make sure you have a micro usb cable to upgrade with
   + For JEM, connect jumper wires between LED_IN pin and GND and then reset board to force JEM into bootloader mode
      + If you don't do this before running the Pycom firmware upgrade application JEM won't upgrade
   + Make sure to use the legacy firmware mentioned above and not the firmware Pycom automatically assignes 

## JEM MicroPython API Upgrade Instructions
### Using micro usb cable
- To upgrade JEM with the latest JEM API install [Atom](https://atom.io/)
- Then install the Pycom [Pymakr plugin](https://atom.io/packages/pymakr) for Atom
- Plug in the JEM via micro usb and power on
- Connect using the 'global settings' Pymakr tab and updating 'device address' with JEM device path
   + For example (on Mac or Linux): 
      + Find your device path: ls /dev/tty. (press tab to see the options)
      + Example: /dev/tty.usbserial-DO0036EU
- Click 'Connect' in the Pymakr toolbar and verify that MicroPython debug text starts popping up
- Download the latest JEM API code from: https://github.com/jem-io/micropython/tree/main/api/jem
- Open jem_api directory with Atom then click on the 'upgrade' button in the Pymakr plugin toolbar below
- Atom should now start uploading latest JEM API to your JEM device (it may take a minute) 
- Atom will restart your JEM board for you after upgrade
- That's it!

   
### BLE Communication test
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
