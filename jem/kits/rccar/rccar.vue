<template>
  <div>
    <div style="display: flex;">
    <div style="flex: 1;">
  <v-card>
  <v-card-title>CYBERBEAST RC</v-card-title>
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  <v-btn class="ma-2" @click="enableStrafe"> {{ EnableStrafeMessage }} 
                  </v-btn> <v-btn class="ma-2" @click="toggleMotion"> {{ ControlTypeMessage }} </v-btn>
                </v-list-item-title>
              </v-list-item-content>
             </v-list-item>
            
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  Forward: {{ frwdMotion }} / Turn: {{ turnMotion }}
                </v-list-item-title>
              </v-list-item-content>
             </v-list-item>
          </v-list>
   </v-card>
  <v-card>
  <v-card-title>Joystick</v-card-title>
    <div :style="joysticksContainerStyle">
      <div :style="topJoysticksStyle">
        <div v-for="index in [0]" :key="index" :style="joystickStyle" ref="joysticks" @mousedown="startTracking(index, $event)" @mouseup="stopTracking(index)" @mousemove="trackMovement(index, $event)" @touchstart="startTracking(index, $event)" @touchmove="trackMovement(index, $event)" @touchend="stopTracking(index)">
          <div :style="outerCircleStyle">
            <div :style="innerCircleStyle(index)"></div>
          </div>
        </div>
      </div>
    </div>
  </v-card>
  </div>
      <div style="flex: 1;">
      <v-card>
        <v-card-title>Sensor Data</v-card-title>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Type</th>
                <th class="text-left">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(data, index) in sensorData" :key="index">
                <td>{{ data.type }}</td>
                <td>{{ data.value }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </div>
  </div>
  </template>
  
  <script>
  const LeftJoystickIndex = 0;
  const RightJoystickIndex = 1;
  module.exports = {
    name: 'Joystick1',
    props: ['parent'],
    data() {
      return {
        forwardThreshold: 6,
        rightThreshold: 6,
        forwardDamping: 1.1,
        rightDamping: 0.6,
        stopRequested: false,
        auxReceived: false,
        motionX: 0,
        motionY: 0,
        EnableStrafeMessage: "Enable Strafe",
        ControlTypeMessage: "Use Phone",
        phoneMotionEn: false,
        strafeEnabled: false,
        sendControlTimer: null,
        rightIntensity: 0,
        forwardIntensity: 0,
        prevRightIntensity: 0,
        prevForwardIntensity: 0,
        joysticks: [
          { tracking: false, startX: 0, startY: 0, currentX: 0, currentY: 0, prevY: 0, prevX: 0 },
        ]
        sensorData: [
      { type: 'Sensor 1', value: 0 },
      { type: 'Sensor 2', value: 0 },
      { type: 'Sensor 3', value: 0 },
      { type: 'Sensor 4', value: 0 },
    ],
      };
    },
    computed: {
      frwdMotion()
      {
        if(this.phoneMotionEn)
        {
          return this.motionX;
        }
        else
        {
          return this.forwardIntensity;
        }
      },
      
      turnMotion()
      {
        if(this.phoneMotionEn)
        {
          return this.motionY;
        }
        else
        {
          return this.rightIntensity;
        }
      },
      
      appStyle() {
        return {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        };
      },
      
      joysticksContainerStyle() {
        return {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        };
      },
      topJoysticksStyle() {
        return {
          display: 'flex',
          justifyContent: 'space-around',
          width: '100%',
          marginBottom: '15%',
        };
      },
      bottomJoystickStyle() {
        return {
          display: 'flex',
          justifyContent: 'center',
        };
      },
      joystickStyle() {
        return {
          width: '100vmin',
          height: '100vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        };
      },
      outerCircleStyle() {
        return {
          backgroundColor: 'green',
          borderRadius: '100%',
          width: '50vmin',
          height: '50vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        };
      },
      innerCircleStyle() {
        return index => ({
          backgroundColor: 'grey',
          borderRadius: '50%',
          width: '10vmin',
          height: '10vmin',
          transform: `translate(${this.joysticks[index].currentX}px, ${this.joysticks[index].currentY}px)`,
        });
      }
    },
    mounted() {
      this.parent.device.rcService.handleAuxResp = this.handleAuxResp;
    },
    
    methods: {  
      async waitForAuxData()
      {
        return new Promise((resolve)=>{
            let count = 0;
            let t = setInterval(()=>{
                if(this.auxReceived)
                {
                   resolve(true);
                   clearTimeout(t);
                   console.log("resolve");
                }
                else if(count++ >= 1000)
                {
                  clearTimeout(t);
                  console.log("done");
                }
                
            }, 5);
        });
  
      },
      
      handleAuxResp(data){
        console.log("got data: " + data);
        this.auxReceived = true;
      },
      
      toggleMotion()
      {
        if(!this.phoneMotionEn)
        {
          console.log("kit startMotion");
          this.parent.startMotion(this.motionHandler);
          this.ControlTypeMessage = "Use Joystick";
          this.phoneMotionEn = true;
          if(this.sendControlTimer == null)
          {
            clearTimeout(this.sendControlTimer);
            this.startSendControlCmd();
          }
        }
        else 
        {
          console.log("kit stopMotion");
          this.parent.stopMotion();
          this.ControlTypeMessage = "Use Phone";
          this.motionX = 0;
          this.motionY = 0; 
          this.stopRequested = true;
          this.phoneMotionEn = false;
        }
      },
      
      motionHandler: function(accelEvent){
        if(this.phoneMotionEn)
        {
            let gScale = 9.81; // gravity = 9.81 m/s^2
            this.motionX = parseInt(100 * accelEvent.accelerationIncludingGravity.x / gScale); //ex: 9.81/9.81 * 100 = 100%
            this.motionY = parseInt(-1 * 100 * accelEvent.accelerationIncludingGravity.y / gScale);
          }
          else {
            this.motionX = 0;
            this.motionY = 0;
          }
      },
      enableStrafe()
      {
        console.log("Enable Strafe")
        if(this.EnableStrafeMessage == "Enable Strafe")
        {
          this.EnableStrafeMessage = "Disable Strafe"
          this.strafeEnabled = true;
        }
        else 
        {
          this.EnableStrafeMessage = "Enable Strafe"
          this.strafeEnabled = false;
        }
      },
  
      async startSendControlCmd()
      {
        console.log("startSendControlCmd");
        this.sendControlTimer = -1;
  
        let frwd = this.forwardIntensity;
        let right = this.rightIntensity;
        
        if(this.stopRequested)
        {
          console.log("stop Requested");
          clearTimeout(this.sendControlTimer); // then cancel next timer callback
          this.sendControlTimer = null;
          this.stopRequested = false;
          let cmd = this.controlMotors(0, 0);
          this.auxReceived = false;
          let resp = await this.parent.device.send(cmd);
          resp = await this.waitForAuxData();
          return;
        }
        
        if(this.phoneMotionEn)
        {
          frwd = this.motionX;
          right = this.motionY;
          if(frwd != this.prevForwardIntensity || right != this.prevRightIntensity)
          {
            this.prevRightIntensity = right;
            this.prevForwardIntensity = frwd;
            let cmd = this.controlMotors(frwd, right);
            console.log("phone send");
            this.auxReceived = false;
            let resp = await this.parent.device.send(cmd);
            resp = await this.waitForAuxData();
            console.log("got resp!");
          }
        }
        else if(frwd!= this.prevForwardIntensity || right != this.prevRightIntensity)
        {
            console.log("send f: " + frwd);
            console.log("send r: " + right);
            this.prevRightIntensity = right;
            this.prevForwardIntensity = frwd;
            let cmd = this.controlMotors(frwd, right);
            console.log("get resp");
            this.auxReceived = false;
            let resp = await this.parent.device.send(cmd);
            resp = await this.waitForAuxData();
            console.log("got resp!");
        }
  
        
        this.sendControlTimer = setTimeout(() => {
          this.startSendControlCmd();
        }, 10);
        
      },
  
    controlMotors(forwardIntensity, rightIntensity) {
      
      // Initialize wheel speeds
      let leftWheelSpeed = 0;
      let rightWheelSpeed = 0;
      
      // apply threshold
      // ex: if forward = 5 and threshold is 6, then forward = 0
      if(this.forwardThreshold >= Math.abs(forwardIntensity)) 
      {
        forwardIntensity = 0;
      }
      if(this.rightThreshold >= Math.abs(rightIntensity))
      {
        rightIntensity = 0;
      }
          
      // apply damping only if no strafe en
      if(!this.strafeEnabled)
      {
         // only apply damping for forward if right is 0 and same for right damping
         forwardIntensity = rightIntensity != 0 ? forwardIntensity * this.forwardDamping : forwardIntensity; //ex: 100% * 0.75 = 75%
         forwardIntensity = parseInt(forwardIntensity); // make sure whole number
        
         rightIntensity = forwardIntensity != 0 ? rightIntensity * this.rightDamping : rightIntensity; //ex: 100% * 0.75 = 75%
         rightIntensity = parseInt(rightIntensity); // make sure whole number
      }
      
      // Ensure intensities are within the allowed range
      forwardIntensity = Math.max(-100, Math.min(100, forwardIntensity));
      rightIntensity = Math.max(-100, Math.min(100, rightIntensity));
      
      if (forwardIntensity !== 0 && rightIntensity === 0) {
          // Move forward or backward without turning
          leftWheelSpeed = rightWheelSpeed = forwardIntensity;
      } else if (forwardIntensity === 0 && rightIntensity !== 0) {
          // Turn in place
          leftWheelSpeed = rightIntensity;
          rightWheelSpeed = -rightIntensity;
      } else if (forwardIntensity !== 0 && rightIntensity !== 0) {
          // Move and turn
          leftWheelSpeed = Math.min(100, Math.max(-100, forwardIntensity + rightIntensity));
          rightWheelSpeed = Math.min(100, Math.max(-100, forwardIntensity - rightIntensity));
      }
  
      // Create the controls object
      let controls = null;
      if(this.strafeEnabled)
      {
        controls = {
            'left_back_motor': forwardIntensity - rightIntensity,
            'right_front_motor': forwardIntensity - rightIntensity,
            'left_front_motor': forwardIntensity + rightIntensity,
            'right_back_motor': forwardIntensity + rightIntensity
        };
      }
      else 
      {
        controls = {
          'left_back_motor': leftWheelSpeed,
          'right_front_motor': rightWheelSpeed,
          'left_front_motor': leftWheelSpeed,
          'right_back_motor': rightWheelSpeed
      };
      }
  
      let left_back_motor = controls['left_back_motor'] >= 0 ? 0b00010000 : 0b00100000;
      let right_front_motor = controls['right_front_motor'] >= 0  ?  0b00000010 : 0b00000001;
      let left_front_motor = controls['left_front_motor'] >= 0  ? 0b00000100 : 0b00001000;
      let right_back_motor = controls['right_back_motor'] >= 0 ? 0b10000000 : 0b01000000;
  
  
      let pwmC = Math.abs(controls['left_back_motor']);//controls['left_back_motor']['speed'];
      let pwmB = Math.abs(controls['right_front_motor']);//controls['right_front_motor']['speed'];
      let pwmA = Math.abs(controls['left_front_motor']);//controls['left_front_motor']['speed'];
      let pwmD = Math.abs(controls['right_back_motor'] );//controls['right_back_motor']['speed'];
  
      let driverOutput = left_back_motor | right_front_motor | left_front_motor | right_back_motor;
  
      // Return the controls object
      //let cmd = `kit._kit.car.update(${driverOutput}, ${pwmA}, ${pwmB}, ${pwmC}, ${pwmD})\n\r`;
      let cmd = `mtr(${driverOutput},${pwmA},${pwmB},${pwmC},${pwmD})\n\r`;
      function dec2bin(dec) {
        return (dec >>> 0).toString(2);
      }
      console.log(dec2bin(driverOutput));
      console.log(cmd);
      return cmd;
    },
  
  
      getClientPosition(event) {
        if (event.type.startsWith('touch')) {
          return {
            clientX: event.touches[0].clientX,
            clientY: event.touches[0].clientY
          };
        }
        return {
          clientX: event.clientX,
          clientY: event.clientY
        };
      },
  
      startTracking(index, event) {
        event.preventDefault();
        const { clientX, clientY } = this.getClientPosition(event);
        const joystickRef = this.$refs.joysticks[index];
        const rect = joystickRef.getBoundingClientRect();
        this.joysticks[index].startX = clientX;
        this.joysticks[index].startY = clientY;
        this.joysticks[index].tracking = true;
        this.trackMovement(index, event);
      },
      trackMovement(index, event) {
        event.preventDefault();
        if (!this.joysticks[index].tracking) return;
        const { clientX, clientY } = this.getClientPosition(event);
        const joystickRef = this.$refs.joysticks[index] || this.$refs.joystick2;
        const rect = joystickRef.getBoundingClientRect();
  
        // Calculate the relative position within the joystick
        let deltaX = clientX - rect.left - rect.width / 2;
        let deltaY = clientY - rect.top - rect.height / 2;
  
        // Apply constraints to keep the inner circle within the joystick bounds
        let maxRadius = rect.width / 2;
        let distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (distance > maxRadius) {
          let angle = Math.atan2(deltaY, deltaX);
          deltaX = Math.cos(angle) * maxRadius;
          deltaY = Math.sin(angle) * maxRadius;
        }
  
        this.joysticks[index].prevX = this.joysticks[index].currentX;
        this.joysticks[index].prevY = this.joysticks[index].currentY;
        this.joysticks[index].currentX = deltaX;
        this.joysticks[index].currentY = deltaY;
        this.updateJoystick(index);
      },
      updateJoystick(index) {
  
        const joystickRef = this.$refs.joysticks[index];
        let angleRadians = Math.atan2(this.joysticks[index].currentY, this.joysticks[index].currentX);
        let angleDegrees = angleRadians * (180 / Math.PI);
        let adjustedAngle = (360 - angleDegrees) % 360;
        let currentRadius = Math.sqrt(this.joysticks[index].currentX * this.joysticks[index].currentX + this.joysticks[index].currentY * this.joysticks[index].currentY);
        let maxRadius = joystickRef.offsetWidth / 4;
        let radiusRatio = Math.min(currentRadius / maxRadius, 1);
        let radiusPercent = radiusRatio * 100;
        let data = { x: this.joysticks[index].currentX, y: this.joysticks[index].currentY, angle: adjustedAngle, radius: currentRadius};
        let xPercent = parseInt(100 * this.joysticks[index].currentX/maxRadius);
        let yPercent = parseInt(100 * this.joysticks[index].currentY/maxRadius);
        let diffX = Math.abs(parseInt(this.joysticks[index].prevX - this.joysticks[index].currentX));
        let diffY = Math.abs(parseInt(this.joysticks[index].prevY - this.joysticks[index].currentY));
        let changed = false;
  
        if(diffY)
        {
            // forward/backward control is left joystick
            changed = true;
            let sign = Math.sign(yPercent);
            this.forwardIntensity = -1* (Math.abs(yPercent) >= 100 ? sign * 100 : yPercent); 
            console.log({ x: this.joysticks[index].currentX, y: this.joysticks[index].currentY, angle: adjustedAngle, radius: currentRadius, radiusPercent });
        }
        if(diffX)
        {
            // left/right control is right joystick
            changed = true;
            let sign = Math.sign(xPercent);
            this.rightIntensity = Math.abs(xPercent) >= 100 ? sign * 100 : xPercent; 
            console.log({ x: this.joysticks[index].currentX, y: this.joysticks[index].currentY, angle: adjustedAngle, radius: currentRadius, radiusPercent });
        }
  
        if(changed && this.sendControlTimer == null)
        {
            console.warn("new!!");
            this.startSendControlCmd();
        }
      },
      stopTracking(index) {
        this.joysticks[index].tracking = false;
        this.joysticks[index].currentX = 0;
        this.joysticks[index].currentY = 0;
        this.forwardIntensity = 0; 
        this.rightIntensity = 0; 
        if(!this.phoneMotionEn)
        {
          this.stopRequested = true;
          console.warn("stop");
        }
      }
    }
  };
  </script>
  
