<template>
  <div id="RCWindow">
  <p>WindowKit</p>
  <v-color-picker dot-size="25" swatches-max-height="200" v-model="color"></v-color-picker>
    <table class="disable-select">
      <tr v-for="(row) in rows" :key="row">
        <td v-bind:class="getClassNameFromRow(row, 0)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">1</td>
        <td v-bind:class="getClassNameFromRow(row, 1)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">2</td>
        <td v-bind:class="getClassNameFromRow(row, 2)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">3</td>
        <td v-bind:class="getClassNameFromRow(row, 3)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">4</td>
        <td v-bind:class="getClassNameFromRow(row, 4)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">5</td>
        <td v-bind:class="getClassNameFromRow(row, 5)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">6</td>
        <td v-bind:class="getClassNameFromRow(row, 6)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">7</td>
        <td v-bind:class="getClassNameFromRow(row, 7)" @mousedown="mouseDown" @mousemove="mouseMove" @mouseup="mouseUp" v-on:click="clickPixel">8</td>
      </tr>
    </table>
  </div>
</template>

<script>
//import { Device } from '../store/projects.js';
module.exports = {
  name: 'window-kit',
  props: ['parent', 'response', 'auxResponse'],
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
    rows: [0, 1, 2, 3, 4, 5, 6, 7],
  }),

  methods: {
    getClassNameFromRow(row, col){
      let id = row*this.rows.length + col; //ex: 0*8 + 0 = 0, 1*8 + 0 = 8
      return "px" + id.toString();
    },

    mouseMove(event) {
      if(this.painting){
        let id = parseInt(event.target.className.split("px")[1]);
        if(this.prevId == id){
          console.log(event.clientX, event.clientY);
        }
        else {
          this.prevId = id;
          this.clickPixel(event);
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
      //disable any leds examples running on kit (like button triggered led thread)
      console.log("prepareKit!!!!")
      this.device.rcService.sendCommand("kit._run = False");
    },

    clearDisplay(){
        //clear_display
        if(this.device.isConnected()){
          this.device.rcService.sendCommand(`kit.neopixel.clear_display()`);
        }
    },

    sendPixel(id, rgb_color){
      //id = pixel number on grid (ex: 0)
      //rgb_color = [0, 0, 0] for OFF or you can send actual color like [12, 45, 39]
      //Only send if color changed
      if(this.prevId == id){
        if(this.prevRgbColor && this.prevRgbColor[0] == rgb_color[0] && this.prevRgbColor[1] == rgb_color[1] && this.prevRgbColor[2] == rgb_color[2]){
          return;
        }
        else{
          this.prevRgbColor = rgb_color;
        }
      }
      else{
        this.prevId = id;
      }
      console.log("sendPixel: " + parseInt(id));
      //console.log(rgb_color);
      //TODO: send color to JEM over ble
      if(this.device.isConnected()){
        if(!this.kitReady){
          this.prepareKit();
          this.kitReady = true;
        }
        let r = parseInt(rgb_color[0]);
        let g = parseInt(rgb_color[1]);
        let b = parseInt(rgb_color[2]);
        //let hexColor = this.rgbToHex(r, g, b); //ex: [1,2,3] => '0x010203'
        this.parent.device.rcService.sendCommand(`kit.neopixel.set_pixel(${id}, (${r}, ${g}, ${b}))`);
      }else {
        console.warn("sendPixel ignored - Device not connected");
      }
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
      console.log("className: " + event.target.className);
      let pixel_id = parseInt(event.target.className.split("px")[1]);
      console.log("pixel id: " + pixel_id);
      let pixel = {id: pixel_id, color: [0, 0, 0]}
      if(event.target.style.backgroundColor == rgbStr){ //if clicked on pixel and we did choose new color then set off
        event.target.style.backgroundColor = "white";
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

<style>
#RCWindow
{
    cursor: pointer;
}
table, th, td {
  border: 1px solid rgb(247, 241, 241);
}
th, td {
  background-color: #96D4D4;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

.disable-select {
    user-select: none; /* supported by Chrome and Opera */
   -webkit-user-select: none; /* Safari */
   -khtml-user-select: none; /* Konqueror HTML */
   -moz-user-select: none; /* Firefox */
   -ms-user-select: none; /* Internet Explorer/Edge */
}

</style>

