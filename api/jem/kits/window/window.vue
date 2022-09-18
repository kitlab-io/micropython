<template>
  <div id="WindowKit" :style="{'cursor': 'pointer'}">
  <p>WindowKit</p>
  <v-color-picker dot-size="25" swatches-max-height="200" v-model="color"></v-color-picker>
    <table :style="tableStyleObject" ref="pixelTable">
      <tr v-for="(row) in rows" :key="row">
        <td v-bind:class="getClassNameFromRow(row, 0)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 1)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 2)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 3)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 4)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 5)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 6)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
        <td v-bind:class="getClassNameFromRow(row, 7)" :style="cellStyleObject" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel"></td>
      </tr>
    </table>

    <!---- timeline slider for frames ----->
    <v-btn depressed v-on:click="addCurrentFrameToTimeline"> Save Frame </v-btn>
    <v-btn depressed v-on:click="clearFrame"> Clear </v-btn>
    <div  v-if="!loopingEn">
    <v-btn depressed v-on:click="loopTimeline"> Loop </v-btn>
    </div>
    <div  v-if="loopingEn">
    <v-btn depressed v-on:click="stopLoopTimeline"> Stop </v-btn>
    </div>
    <v-btn depressed v-on:click="clearLoop"> Clear Loop </v-btn>
    <v-btn v-on:click="getKitFeatures">Get Features</v-btn>
    <!---- features buttons ------>
    <v-btn v-for="button in buttons" :key="button.title" v-on:click="callFeatureButton(button.func)">{{ button.title }}</v-btn>
    <v-slider v-for="slider in sliders" :key="slider.title"
            v-model="slider.value"
            @change="slider.onChange"
            :min="slider.min"
            :max="slider.max"
            :label="slider.title"
            >
    </v-slider>


    <v-slider
      v-model="timeline.val"
      hint="Timeline"
      :min="timeline.min"
      :max="timeline.max"
      @change="timelineChanged"
      thumb-label="always"
      :thumb-color="timeline.color"
      :thumb-size="24"
      step="1"
      ticks="always"
      tick-size="10"
      label="Timeline"
      ></v-slider>
  </div>
</template>

<script>
module.exports = {
  name: 'WindowKit',
  props: ['parent'],
  components: {
    // GithubCorner
  },
  data: () => ({
    size: 8,
    color: "#FF00FF",
    index: 0,
    kitReady: false,
    prevId: null,
    prevRgbColor: null,
    painting: false,
    pixelPadNbsp: "&nbsp;&nbsp;&nbsp;&nbsp;",
    frameTimeline: [],
    buttons: [],
    sliders: [],
    loopIndex: 0,
    loopingEn: false,
    frame: Array(64),
    timeline: { min: 0, max: 0, label: 'color', val: 0, color: 'orange darken-3' },
    rows: [0, 1, 2, 3, 4, 5, 6, 7],
    cellStyleObject: {
      'background-color': '#96D4D4',
      'padding-top' : '10px',
      'padding-bottom' : '10px',
      'padding-left' : '10px',
      'padding-right' : '10px'
    },
    tableStyleObject: {
      border: '1px solid rgb(247, 241, 241)',
      'user-select' : 'none', /* supported by Chrome and Opera */
      '-webkit-user-select' : 'none', /* Safari */
      '-khtml-user-select' : 'none', /* Konqueror HTML */
      '-moz-user-select' : 'none', /* Firefox */
      '-ms-user-select' : 'none', /* Internet Explorer/Edge */
    }
  }),

  mounted(){
    console.log('starting windowkit');
    this.clearFrame();
    this.parent.device.rcService.handleResp = this.kitResponseHandler
    this.prepareKit();
  },

  methods: {
    kitResponseHandler(resp){
      let featuresJson = JSON.parse(resp)
      this.buttons = featuresJson.buttons;
      if(featuresJson.sliders){
        this.sliders = featuresJson.sliders;
        for(let s in this.sliders){
          this.sliders[s].onChange = (v)=>{
            let slider = this.sliders[s];
            this.sliderOnChange(slider, v);
            }; //attach a callback to each slider so we can handle changed value
        }
      }
    },

    sliderOnChange(slider, v){
      console.log("slider %s changed to %s: ", slider.func, v);
      let cmdStr = String(`${slider.func}(${v})`);
      console.log("cmdStr: " + cmdStr);
      this.sendCommand(cmdStr);
    },

    async getKitFeatures(){
      await this.sendCommand('from kits.window.window import *');
      await this.parent.device.rcService.sendEvalCommand('features_json');
    },

    async callFeatureButton(func_name){
      await this.sendCommand(func_name + "()");
    },

    async loopCallback()
    {
        await this.loadFrame(this.frameTimeline[this.loopIndex]);
        this.loopIndex = (this.loopIndex + 1) % this.frameTimeline.length;
        //now repeat loop
        if(this.loopingEn){
          this.loopTimer = setTimeout(this.loopCallback, 400);
        }
    },
    stopLoopTimeline(){
      this.loopingEn = false;
    },

    loopTimeline(){
      console.log("loopTimeline");
      this.loopIndex = 0;
      this.loopingEn = true;
      this.loopTimer = setTimeout(this.loopCallback, 50);
    },

    clearLoop(){
      console.log("clearLoop");
      this.frameTimeline = []; //clear timeline and replace with blank
      this.timeline.max = 0;
      this.clearFrame();
    },

    featureSliderChange(v){
      console.log("featureSliderChange to: " + v);
    },

    timelineChanged(v){
      console.log("timelineChanged to: " + v);
      this.loadFrame(this.frameTimeline[v]);
    },

    loadFrame(frame){
      for(let i = 0; i<frame.length; i++){
        let col = i % this.size; //0 % 8 = 0, 8 % 8 = 0, 8 % 9 = 1
        let row = parseInt(i / this.size); //0 / 8 = 0, 8/8 = 1, 9/8 = 1 ... 63/8 = 7
        let rgb = frame[i];
        let rgbStr = "rgb(" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + ")";
        console.log(`row ${row}, col ${col}`)
        console.log("style: " + this.$refs.pixelTable.childNodes[row].childNodes[col].style);
        this.$refs.pixelTable.childNodes[row].cells[col].style.backgroundColor = rgbStr;
      }
      this.sendFrame(frame); //send to device to display
    },

    clearFrame(){
      for(let i = 0; i<this.frame.length; i++){
        this.frame[i] = [0,0,0];
      }
      this.loadFrame(this.frame);
    },

    addCurrentFrameToTimeline(){
      console.log("addCurrentFrameToTimeline %d", this.frameTimeline.length);
      let newFrame = Array(this.size*this.size);
      for (let i = 0; i < newFrame.length; i++) {
        newFrame[i] = this.frame[i];
      }
      this.frameTimeline.push(newFrame);
      this.timeline.max = this.frameTimeline.length - 1;
      this.timeline.val = this.timeline.max;
    },

    addPixelToFram(id, rgb_color){
      this.frame[id] = [parseInt(rgb_color[0]), parseInt(rgb_color[1]), parseInt(rgb_color[2])];
    },

    getClassNameFromRow(row, col){
      let id = row*this.rows.length + col; //ex: 0*8 + 0 = 0, 1*8 + 0 = 8
      return "px" + id.toString();
    },

    mouseMove(event) {
      if(this.painting){
        let id = parseInt(event.target.className.split("px")[1]);
        if(this.prevId == id){
          //console.log(event.clientX, event.clientY);
        }
        else {
          this.clickPixel(event);
          this.prevId = id;
        }
      }
    },
    mouseUp(event) {
      this.painting = false;
    },
    mouseDown(event) {
      this.painting = true;
    },

    prepareKit(){
      //import kit functions to micropython runtime if not done already
      if(this.parent.device.isConnected()){
        this.parent.device.rcService.sendCommand('from kits.window.window import *');
      }
    },

    clearDisplay(){
        //clear_display
        if(this.parent.device.isConnected()){
          this.sendCommand(`kit_helper.neopixel.clear_display()`);
        }
    },

    async sendFrame(frame){
      /*
      frameStr = "[ (0,225,123), (123,0,9), (45,67,98) ... ]"
      device.sendCommand("kit_helper.neopixel.data = ${frameStr}")
      device.sendCommand("kit_helper.neopixel.show(kit.neopixle.data)")
      */
      let frameStr = "[";
      for(let i = 0; i<frame.length; i++){
        let colorStr = `(${frame[i][0]}, ${frame[i][1]}, ${frame[i][2]}),`
        frameStr += colorStr;
      }
      frameStr += "]";
      if(this.parent.device.isConnected()){
        await this.sendCommand(`kit_helper.neopixel.data = ${frameStr}`);
        return this.sendCommand(`kit_helper.neopixel.chain.show(kit_helper.neopixel.data)`);

      }
      else {
        console.warn("sendFrame ignored - Device not connected");
      }
      return new Promise((resolve) => {resolve(false);});
    },

    sendPixel(id, rgb_color){
      //id = pixel number on grid (ex: 0)
      //rgb_color = [0, 0, 0] for OFF or you can send actual color like [12, 45, 39]
      //Only send if color changed
      console.log("sendPixel: " + parseInt(id));
      console.log("this.prevId: " + this.prevId);
      this.addPixelToFram(id, rgb_color);
      if(this.prevId == id){
        if(this.prevRgbColor && this.prevRgbColor[0] == rgb_color[0] && this.prevRgbColor[1] == rgb_color[1] && this.prevRgbColor[2] == rgb_color[2]){
          console.log("ignore")
          return;
        }
        else{
          this.prevRgbColor = rgb_color;
        }
      }
      else{
        this.prevId = id;
      }

      console.log("sending: " + parseInt(id));
      //console.log(rgb_color);
      //TODO: send color to JEM over ble
      if(this.parent.device.isConnected()){
        let r = parseInt(rgb_color[0]);
        let g = parseInt(rgb_color[1]);
        let b = parseInt(rgb_color[2]);
        //let hexColor = this.rgbToHex(r, g, b); //ex: [1,2,3] => '0x010203'
        //this.parent.device.rcService.sendCommand(`kit.jem.led.set_color(${hexColor})`); //ex: set_color(0x110022)
        this.sendCommand(`kit_helper.neopixel.set_pixel(${id}, (${r}, ${g}, ${b}))`);
      }else {
        console.warn("sendPixel ignored - Device not connected");
      }
    },

    sendCommand(cmdStr){
      if(!this.kitReady){
          this.prepareKit();
          this.kitReady = true;
      }
      this.parent.device.rcService.sendCommand(cmdStr);
    },

    rgbToHex(r, g, b) {
      return "0x" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
    },

    hexToRgb(hex) {
      var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
      } : null;
    },

    clickPixel(event){
      //this.color is a hex value like: #050709 but we need to convert to 'rgb(5, 7, 9)'
      let rgb = this.hexToRgb(this.color);
      let rgbStr = "rgb(" + rgb.r + ", " + rgb.g + ", " + rgb.b + ")";
      let pixel_id = parseInt(event.target.className.split("px")[1]);
      let pixel = {id: pixel_id, color: [0, 0, 0]}
      if(event.target.style.backgroundColor == rgbStr){ //if clicked on pixel and we did choose new color then set off
        event.target.style.backgroundColor = "black";
      }
      else
      {
        event.target.style.backgroundColor = rgbStr;//otherwise update to new color
        pixel.color[0] = rgb.r;
        pixel.color[1] = rgb.g;
        pixel.color[2] = rgb.b;
      }
      this.sendPixel(pixel.id, pixel.color);
    }
  }
}
</script>
