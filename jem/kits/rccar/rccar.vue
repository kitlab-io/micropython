<template>
  <div id="RCcar" :style="{'cursor': 'pointer'}">
  <p>RC-CAR</p>

    <!---- Move Buttons ----->
    <v-btn depressed v-on:click="stopMotion"> StopMotion </v-btn>
    <v-btn depressed v-on:mousedown="forward" v-on:mouseup="stopMotion"> Forward </v-btn>
    <v-btn depressed v-on:mousedown="backward" v-on:mouseup="stopMotion"> Backward </v-btn>
    <v-btn depressed v-on:mousedown="left" v-on:mouseup="stopMotion"> Turn Left </v-btn>
    <v-btn depressed v-on:mousedown="right" v-on:mouseup="stopMotion"> Turn Right </v-btn>
	
    <!-- Color Slider -->
  	<input type="range" min="0" max="1023" v-model="speed" @input="setspeed"> 
  
  </div>
</template>

<script>
module.exports = {
  name: 'RCcar',
  props: ['parent'],
  components: {
    // GithubCorner
  },
  data: () => ({
    kitReady: false,
    speed: 0,
    speedTimer: null
  }),

  mounted(){
    console.log('starting RCcar kit');
    this.parent.device.rcService.handleResp = this.kitResponseHandler
    this.prepareKit();
  },

  methods: {
    setspeed() {
       
       // NOTE: make sure you include newline and carriage return \n\r in your cmd since using the REPL
       let cmd = `kit._kit.car.set_speed(${this.speed})\n\r`; // create the micropython cmd to set buzzer
       if(this.speed == 0){
          cmd = `kit._kit.car.stop()\n\r`; // if freq 0 just stop buzzer
       }

       if(this.speedTimer){
           clearTimeout(this.speedTimer); // if we already have a cmd pending, cancel it and use latest one
       }
       this.speedTimer = setTimeout(()=>{ this.parent.device.send(cmd) }, 100); // send raw MicroPython REPL cmd after 100 millisec
    },
    
    kitResponseHandler(resp){
      console.log("kit response " + resp);
    },

    stopMotion(){
      console.log("kit stopMotion");
      this.sendCommand("kit._kit.car.stop()");
    },

    forward(){
      console.log("forward");
      this.sendCommand("kit._kit.car.forward()")
    },

    backward(){
      console.log("backward");
      this.sendCommand("kit._kit.car.backward()")
    },
    left(){
      console.log("left");
      this.sendCommand("kit._kit.car.left()")
    },
    right(){
      console.log("right");
      this.sendCommand("kit._kit.car.right()")
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
