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
  