<template>

  <div id="SimpleKitTemplate" :style="{'cursor': 'pointer'}">
  <p>Simple Kit</p>
  
  <!-- Example Buttons -->
  <v-btn @click="startRangeRead">{{ readRangeMsg }}</v-btn>
  <v-btn @click="ledRed">LED RED</v-btn>
  <v-btn @click="ledOff">LED OFF</v-btn>

  <!-- Color Slider -->
  <input type="range" min="0" max="360" v-model="hue" @input="setColorFromSlider">    
  
  <!-- Range Sensor -->
  <v-progress-linear v-model="range" color="blue" height="25"> {{ range }} </v-progress-linear>
    
  </div>
</template>

<script>
const startReadRangeMsg = "Start Range Sensing";
const stopReadRangeMsg = "Stop Range Sensing";

module.exports = {
  name: 'SimpleKitTemplate',
  props: ['parent'],

  data: () => ({
    range: 0,
    resp: "",
    
    //freq slider
    rangeTimer: null,
    sliderValue: 0,
    readRangeMsg: startReadRangeMsg,
    //color picker
    hue: 0, // Initial hue value
    selectedColor: 'rgb(255, 0, 0)', // Initial color

  }),

  mounted(){
    console.log('starting demo kit');
    this.parent.device.rcService.handleAuxResp = this.kitAuxRespHandler;
  },

  beforeDestroy() {
      if (this.rangeTimer) {
        clearInterval(this.rangeTimer);
      }
  },

  methods: {
    
  // send color to JEM via Bluetooth rc service
  sendColorFromSlider(colorStr) //ex: colorStr = 'rgb(100, 100, 0)'
  {
    let rgb = colorStr.substr(3); //get '(r,g,b)' from 'rgb(r,g,b)'
    let cmd = `kit._kit.led.set_color(${rgb})`;
      if(this.sendTimer)
        clearTimeout(this.sendTimer);
      this.sendTimer = setTimeout(()=>{this.sendCommand(cmd)}, 100);
  },
  
  // color updates from slider
  setColorFromSlider() {
    // Convert hue to RGB
    this.selectedColor = this.hslToRgb(this.hue / 360, 1, 0.5);
    console.log("setColorFromSlider: " + this.selectedColor);
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

    kitAuxRespHandler(resp){
      let strResp = new TextDecoder().decode(resp);
      this.resp = this.resp.concat(strResp);
      console.log("message from JEM: " + this.resp);
    },
    
    ledRed(){
      console.log("ledRed");
      this.sendCommand("kit._kit.led.set_color((100,0,0))")
    },
    
    ledOff(){
      console.log("ledOff");
      this.sendCommand("kit._kit.led.off()")
    },

    async startRangeRead()
    {
      if(this.readRangeMsg == startReadRangeMsg)
      {
        this.readRangeMsg = stopReadRangeMsg;
        this.rangeTimer = setTimeout(()=>{this.readRange();}, 100);
      }
      else 
      {
        this.readRangeMsg = startReadRangeMsg;
        clearTimeout(this.rangeTimer);
      }
    },
    
    async readRange()
    {
      if(this.readRangeMsg == stopReadRangeMsg)
      {
        let resp = await this.parent.device.rcService.sendEvalCommand("kit._kit.range.distance");
        console.log("readRange = " + resp);
        this.range = parseInt(resp);
        this.rangeTimer = setTimeout(()=>{this.readRange();}, 50);
      }
    },

    sendCommand(cmdStr){
      this.parent.device.rcService.sendCommand(cmdStr);
    },
  }
}
</script>
