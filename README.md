# JEM2 RC Car Kit
- RC Car Kit for JEM2
- Use the kits/rccar/rccar.vue file to edit the RC Car GUI controls
- use the kits/rccar/rccar.py file to tune the RC car motor controls or add features

## Tutorial
### Quickstart
1. Connect JEM to the RC Car Kit Daughter Board
   - Make sure the JEM RGB LED is facing the front of the RC Car Chassis
2. Make sure you have the RC Car Kit lipo battery installed and that it's been charged
   - This may required you to unscrews the battery compartment and install the battery
3. Enable the RC Car power with the power switch
4. Turn on the JEM with the JEM power switch (located next to the JEM RGB LED)
   - Once JEM is ON, you should see a small BLUE led light up
5. Open up the JEM Mobile or Web based App
6. On the 'Pair' page, click on 'BLE Connect' and select your JEM from the available options and wait for connection to finish
   - May take 10 seconds
7. Then click the 'Load All' button to see the official RC Car Kit
8. Click on 'Sync' to upload the RC Car Kit code to the Mobile or Web App
9. Navigate to the 'Editor' page and make sure you see the 'rccar.py' file loaded
10. Navigate to the 'RC' page (remote control) and make sure you see the RC Car Kit GUI
11. Navigate back to the 'Editor' page and select the 'RC Car Kit' project and then scroll all the way down till you see the 'Flash to JEM' button and click that
   - Flashing can take anywhere from 10 seconds to 2 minutes depending on how much new code there is
12. After flashing complete, reconnect and then make sure you have the JEM Board project selected
13. Navigate to the 'RC' page and use the Joystick to control your RC Car
14. If you are using you iPhone you can also click on the 'Use Phone' option
   - This option allows you to control forward / backward motion with your phone tilting forward / backwards
   - You can also control left / right motion by tilting your phone left or right

## JEM Wiki
- see: https://github.com/kitlab-io/micropython/wiki


