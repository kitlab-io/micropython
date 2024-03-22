# JEM Simple Kit
- Kit showing how to use the RGB LED and Range Sensor

## Instructions
- Flash kit to JEM
- Navigate to **RC** tab on Web or Mobile App and control RGB LED and test range sensor
- Edit the **kits/simple/simple.vue** file to update your kit UI and then reload the **RC** tab to see changes live

## Tutorial 1
In this tutorial we can add a new button (called BUZZ) to the kit simple.vue file and have it execute a newly created function in our simple.py kit file that makes a buzzer sound.

- Use code in 'kits/simple/tutorial_1'
   + This sub directory has files that include a new button element in the vue file and a new function in the python file
   + Look for the code between comments 'Tutorial_1' and 'Tutorial_1 !' in each file to see the new code
   ```txt 
         # Tutorial_1
          some new py code
         # Tutorial_1 !

         or 

         // Tutorial_1
         some new js code
         // Tutorial_1 !
   ``` 
- Replace 'simple.py' and 'simple.vue' in 'kits/simple/' with the same files in 'kits/simple/tutorial_1'
- Flash the new code to JEM and reconnect
- Navigate to the 'RC' page and make sure you see a new button called 'BUZZ'
   + If you don't try clicking the reload button (the green circular arrow) at the top left of the 'RC' page
- Click the 'BUZZ' button and make sure it creates a buzzer sound
