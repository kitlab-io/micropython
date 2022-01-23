<template>
<div>
  <h1>{{message}}</h1>
  <button v-on:click="toggle_led" depressed outlined class="fb-btn">Toggle RGB LED</button>
  <h2> {{response}} </h2>
  <h2> {{auxResponse}} </h2>
</div>
</template>
<script>

module.exports={
name: 'tab-test',
props: ['parent', 'response', 'auxResponse'],
data: ()=>(
{
kitname: "LanternKit",
message: 'Dynamic Lantern Kit Component Loaded!',
device: this.test,
color1: "0xFF0000",
color2: "0x0000FF",
color: "0xFF0000"
}),
methods: {
  async toggle_led(){
      console.log("start: " + this.parent.name);
      if(this.color == this.color1){
        this.parent.device.rcService.sendCommand("demo.jem.led.set_color(0x0000FF)");
        this.color = this.color2;
      }
      else {
        this.parent.device.rcService.sendCommand("demo.jem.led.set_color(0xFF0000)");
        this.color = this.color1;
      }
  },

  async setPixel(number, percent, rgb){
      console.log("%s - setPixel", this.name);
      //LanternKit.setPixel(this.device.rcService, 0, 50, 0x112233);
  },

  async setIntensity(rgb, percent){
      console.log("%s - setIntensity", this.name);
      //LanternKit.setIntensity(this.device.rcService, 50);
  },

  async setColorFromOrientation(roll, pitch, yaw){
      console.log("%s - setColorFromOrientation", this.name);
      //LanternKit.setColorFromOrientation(this.device.rcService, 0, 0, 0);
  },

  async setColor(rgb){
      console.log("%s - setColor", this.name);
      //LanternKit.setColor(this.device.rcService, 0x112233);
  }
}
};
</script>
