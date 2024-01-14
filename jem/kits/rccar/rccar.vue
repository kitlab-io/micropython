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
  




<template>

    <div id="DemoKit" :style="{'cursor': 'pointer'}">
    <p>DemoKit</p>
   <div> Buzzer Freq (Hz) </div>
   <input type="range" v-model="buzzFreq" @input="buzzerSliderChanged" min="0" max="2000">
  
  	<div> Change LED Color </div>
      <!---- color picker ----->
     <!-- Color Gradient Bar -->
    <div id="color-bar" @click="setColorFromBar" style="width: 100%; height: 50px; cursor: pointer; background: linear-gradient(to right, #ff0000, #ffff00, #00ff00, #00ffff, #0000ff, #ff00ff, #ff0000);"></div>

    <!-- Color Slider -->
    <input type="range" min="0" max="360" v-model="hue" @input="setColorFromSlider">
    
    <!-- Display Selected Color -->
    <div :style="{ backgroundColor: selectedColor, width: '100px', height: '100px', margin: '20px auto' }"></div>
    <!-- <v-color-picker
        class="ma-2"
        hide-canvas
        update="@color"
        v-model="selectedColor" 
        @input="colorChanged"
      ></v-color-picker> -->
      <div>
      <v-btn elevation="2"
             class="mb-4"
             @click="distanceLedMode"
      >Distance + LED</v-btn>
      <div class="mt-4">Distance</div>
      <v-progress-linear
        v-model="range"
        color="blue"
        height="25"
      >
      {{ range }}
      </v-progress-linear>
      <div>Light</div>
      <v-progress-linear
        v-model="light"
        color="amber"
        height="25"
      >
      {{ light }}
      </v-progress-linear>
      </div>
      <div>
      <v-btn elevation="2"
             class="mt-4"
             @click="motionLedMode"
      >Motion + LED</v-btn>
      </div>
      <div>
      <svg width="200" height="200">
      <path
        :d="getPieChartPath(80, imu.roll)"
        fill="blue"
      />
      <text x="100" y="100" font-size="16" text-anchor="middle" alignment-baseline="middle" fill="white">
        {{ imu.roll }}
      </text>
    </svg>
    <svg width="200" height="200">
      <path
        :d="getPieChartPath(80, imu.pitch)"
        fill="red"
      />
      <text x="100" y="100" font-size="16" text-anchor="middle" alignment-baseline="middle" fill="white">
        {{ imu.pitch }}
      </text>
    </svg>
    <svg width="200" height="200">
      <path
        :d="getPieChartPath(80, imu.yaw)"
        fill="green"
      />
      <text x="100" y="100" font-size="16" text-anchor="middle" alignment-baseline="middle" fill="white">
        {{ imu.yaw }}
      </text>
    </svg> 
      </div>
      <div>
      <v-btn elevation="2"
             class="mb-4"
      	     @click="tempLedMode"
      >Temperature + LED</v-btn>
      <div v-if="atm">pressure (Pa): {{ atm.pressure }}</div>
      <div v-if="atm">temperature (deg C): {{ atm.temp }}</div>
      <div v-if="atm">humidity (%): {{ atm.humidity }}</div>
      <div v-if="atm">altitude (m): {{ atm.altitude }}</div>
	  </div>
    </div>
  </template>
  
  <script>
  module.exports = {
    name: 'DemoKit',
    props: ['parent'],
    components: {
      // GithubCorner
    },
    data: () => ({
      kitReady: false,
      range: 0,
      light: 0,
      imu: {'roll': 0, 'pitch': 0, 'yaw': 0},
      atm: {'temp': 0, 'pressure':0, 'humidity':0, 'altitude':0},
      resp: "",
      
      //freq slider
      freqTimer: null,
      prevBuzzFreq: null,
      buzzFreq: 0,
      buzzSlider: 0,
      sliderValue: 0,
      
      //color pciker
      hue: 0, // Initial hue value
      selectedColor: 'rgb(255, 0, 0)', // Initial color

    }),
  
    mounted(){
      console.log('starting demo kit');
      this.parent.device.rcService.handleResp = this.kitResponseHandler
      this.parent.device.rcService.handleAuxResp = this.kitAuxRespHandler;
      this.prepareKit();
    },
  
    methods: {
      sliderChange() {
        console.log('Slider value changed to: ', this.sliderValue);
        // Implement your logic here using this.sliderValue
      },
      buzzerSliderChanged() {
      // This function will be called whenever the slider value changes.
      // 'newValue' will be the current value of the slider.
      console.log('Slider value changed to: ', this.buzzFreq);

      // Add your custom logic here
      //this.buzzFreq = newValue;
      if(!this.freqTimer)
      {
        this.freqTimer = setInterval(()=>
        {
          if(this.prevBuzzFreq != this.buzzFreq)
          {
            let cmd = `kit._kit.buzz.start(${this.buzzFreq})`;
            if(this.buzzFreq == 0)
            {
              cmd = `kit._kit.buzz.stop()`;
            }

            this.sendCommand(cmd);
            this.prevBuzzFreq = this.buzzFreq;
          }

        }, 100);
      }
    },
      // color picker
    sendColorFromSlider(colorStr) //ex: colorStr = 'rgb(100, 100, 0)'
    {
      let rgb = colorStr.substr(3); //get '(r,g,b)' from 'rgb(r,g,b)'
      let cmd = `kit._kit.global_color=${rgb};kit._kit.color_mode='none'`;
        if(this.sendTimer)
        	clearTimeout(this.sendTimer);
        this.sendTimer = setTimeout(()=>{this.sendCommand(cmd)}, 100);
    },
      
    setColorFromSlider() {
      // Convert hue to RGB
      this.selectedColor = this.hslToRgb(this.hue / 360, 1, 0.5);
      console.log("setColorFromSlider: " + this.selectedColor);
      this.sendColorFromSlider(this.selectedColor);
      
    },
    setColorFromBar(event) {
      const rect = event.target.getBoundingClientRect();
      const x = event.clientX - rect.left; // x position within the element.
      const width = rect.width;
      const hue = Math.round((x / width) * 360);
      this.hue = hue;
      this.selectedColor = this.hslToRgb(hue / 360, 1, 0.5); //'rgb(100,4,39)'
      this.sendColorFromSlider(this.selectedColor);
    },
    hslToRgb(h, s, l) {
      let r, g, b;
      if (s == 0) {
        r = g = b = l; // achromatic
      } else {
        const hue2rgb = (p, q, t) => {
          if (t < 0) t += 1;
          if (t > 1) t -= 1;
          if (t < 1/6) return p + (q - p) * 6 * t;
          if (t < 1/2) return q;
          if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
          return p;
        };
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
      }
      return `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`;
    },
      
      distanceLedMode()
      {
        console.log("distanceLedMode");
        alert("Move hand over range sensor to change led color");
        this.sendCommand("kit._kit.color_mode='range'");
      },
      
      motionLedMode()
      {
        console.log("motionLedMode");
        alert("Rotate JEM in any direction to change led color");
        this.sendCommand("kit._kit.color_mode='imu'");
      },
      
      tempLedMode()
      {
        console.log("temperatureLedMode");
        alert("Change temperature near JEM to change led color");
        this.sendCommand("kit._kit.color_mode='temp'");
      },
      
      colorChanged() {
      // Call your function with the new color
      this.yourFunction(this.selectedColor);
      },
      
      yourFunction(newColor) {
        // Parse the hexadecimal color code into separate R, G, and B components
        const r = parseInt(newColor.slice(1, 3), 16);
        const g = parseInt(newColor.slice(3, 5), 16);
        const b = parseInt(newColor.slice(5, 7), 16);

        // Create the "(r,g,b)" string
        const rgbString = `(${r},${g},${b})`;

        // Do something with the RGB string
        console.log('New color in (r,g,b) format: ' + rgbString);
        let cmd = `kit._kit.global_color=(${r},${g},${b});kit._kit.color_mode='none'`;
        if(this.sendTimer)
        	clearTimeout(this.sendTimer);
        this.sendTimer = setTimeout(()=>{this.sendCommand(cmd)}, 100);
        
      },
      
      // Function to generate the SVG path for a pie chart sector
    getPieChartPath(radius, angle) {
      if(angle >= 360)
      {
        angle = 359.9;
      }
      else if(angle <= -360)
      {
        angle = -359.9;
      }
      const x = 100; // Center of the SVG container
      const y = 100; // Center of the SVG container
      const startAngle = 0;

      // Determine the direction (clockwise or counterclockwise) based on the sign of the angle
      const isClockwise = angle >= 0;
      const absAngle = Math.abs(angle);

      // Calculate the end angle in radians
      const endAngle = (startAngle + (isClockwise ? absAngle : -absAngle)) * (Math.PI / 180);

      // Calculate the coordinates for the start and end points of the arc
      const startX = x + radius * Math.cos(startAngle * (Math.PI / 180));
      const startY = y + radius * Math.sin(startAngle * (Math.PI / 180));
      const endX = x + radius * Math.cos(endAngle);
      const endY = y + radius * Math.sin(endAngle);

      // Determine whether to draw the arc in a large or small arc (clockwise or counterclockwise)
      const largeArcFlag = absAngle > 180 ? 1 : 0;

      // Use the "L" (line) SVG path command to draw lines to the start and end points,
      // and close the path with "Z" to complete the sector
      const pathData = `M ${x} ${y} L ${startX} ${startY} A ${radius} ${radius} 0 ${largeArcFlag} ${isClockwise ? 1 : 0} ${endX} ${endY} Z`;

      return pathData;
    },
      
      kitResponseHandler(resp){
        console.log("kit response " + resp);
      },
  
      kitAuxRespHandler(resp){
        console.log("kit aux response " + resp);
        if(resp.length >= 3 && resp[0] == 1 && resp[1] == 2 && resp[2] == 3)
        {
          console.log("kitAuxRespHandler reset");
          this.resp = ""
          return;
        }
        let strResp = new TextDecoder().decode(resp);
        this.resp = this.resp.concat(strResp);
        console.log("kit aux str response " + this.resp);
        try
        {
          let jsonStr = JSON.parse(this.resp);
          this.range = jsonStr["range"];
          this.light = jsonStr["light"];
          this.imu = jsonStr["imu"];
          this.atm = jsonStr["atm"]
          console.log(jsonStr);
          this.resp = "";  // reset
        }
        catch(e)
        {
          console.warn("kitAuxRespHandler: " + e);
        }
      },
      
      led_red(){
        console.log("led_red");
        this.sendCommand("kit._kit.led_red()")
      },
      led_blue(){
        console.log("led_red");
        this.sendCommand("kit._kit.led_blue()")
      },
  
      prepareKit(){
        //import kit functions to micropython runtime if not done already
        if(this.parent.device.isConnected()){
        }
      },
  
      sendCommand(cmdStr){
        if(!this.kitReady){
            this.prepareKit();
            this.kitReady = true;
        }
        this.parent.device.rcService.sendCommand(cmdStr);
      },
  
    }
  }
  </script>
  
