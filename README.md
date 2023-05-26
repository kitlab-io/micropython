# JEM Micropython Overview
- For general jem tutorial see the main kitlab [jem2 micropython repo readme](https://github.com/kitlab-io/micropython/tree/jem2#use-thonny-micropython-ide)


# SimpleBot Assembly Instructions
- Attach micro servos to each side of the SimpleBot chassis but sliding them up through the server holder and then pushing in so they are snug
   + Note: You may have received an older SimpleBot that requires you to screw on the micro servos with provided screw
- Attach the micro servo wheel traction rubber to each wheel
- Press the wheel agains the micro servo axle until it fits and then use the provided screws to fasten the wheels
- Attach the Battery pack to the end of the chassis (like shown in the diagram below) using the provided velcro strips
- Plug in the battery pack and two servo cables into the SimpleBot daughter board PCB using the diagram below
- Connect the JEM module to the SimpleBot daughter board so that that the JEM circular LED cutout is facing the right side of the daughter board
   + See diagram below
- Turn on your JEM and verify the small blue led turns on (the one on the other side of the circular RGB LED cutout)
- Visit the kitlab [jem web ide](jem.kitlab.io) or open your kitlab jem mobile app
- Click on the 'Load' kits button
- Click on the JEM2 SimpleBot kit button and wait 5 - 10 sec (still need to add progress bar, sorry!)
- Navigate to the 'Edit' tab and notice that you should see a FileExplorer on the left - click on it to view files
- To flash the Kit code to JEM scroll down and click on the 'Flash' button and wait till you are prompted to reconnect
   + make sure NOT to refresh your browser and turn off your JEM during this time or you will have to use a nativate micropython IDE on you computer via USB to re-flash you JEM
- Assuming you flashed the kit code and everything worked navigate to the 'RC' tab to see the SimpleBot controller UI
   + You can use this to control the simple bot and make it move

- Make sure to turn on the SimpleBot AAA batter back before controlling the robot!
- Extra: you can edit the kits/simplebot/simplebot.py file and add more functions and call those extra functions by editing the simplebot.vue file
   + Then flash that code back to the JEM and you should see your updates reflected in the Web App or iOS App
- IMPORTANT! 
   + If at any point your JEM stop working you should power cycle it and then re-flash the code based on [jem2 instructions](https://github.com/kitlab-io/micropython/tree/jem2#use-thonny-micropython-ide)

## SimpleBot chassis assembled
![simplebot-cad](https://docs.google.com/drawings/d/e/2PACX-1vSt_QIv9TH_b58j-GVUd6zhkSzOAC-g2jr5ij1Ajra0lTEjkV_zZSMi223f85wOceEIIfac7JsKApaI/pub?w=960&h=720)

## Servos
![servos](https://docs.google.com/drawings/d/e/2PACX-1vQ0B1CEekowwH7LZ4TfEMPkwIZ_FuRFfY6R265BfTh7P554vkQS8akQVlRfg3sQzEHyGB88PNNMyLUf/pub?w=719&h=395)

## Daughter Board
- Board that JEM connects to and uses to control the servos

![daughter-board](https://docs.google.com/drawings/d/e/2PACX-1vRJJF0rhW87rzehcLenv6fP_xek2_QWFvbxtyNMfcoY4nYM9o4CxKgMo0WO4RB4PL0HWADXnWOdv92_/pub?w=702&h=685)


