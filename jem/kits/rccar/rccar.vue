<template>
  <div id="RCcar" :style="{'cursor': 'pointer'}">
  <p>RC-CAR</p>

    <!---- Move Buttons ----->
    <v-btn depressed v-on:click="stopMotion"> StopMotion </v-btn>
    <v-btn depressed v-on:mousedown="forward" v-on:mouseup="stopMotion"> Forward </v-btn>
    <v-btn depressed v-on:mousedown="backward" v-on:mouseup="stopMotion"> Backward </v-btn>
    <v-btn depressed v-on:mousedown="spin_left" v-on:mouseup="stopMotion"> Turn Left </v-btn>
    <v-btn depressed v-on:mousedown="spin_right" v-on:mouseup="stopMotion"> Turn Right </v-btn>
	<v-btn depressed v-on:mousedown="strafe_left" v-on:mouseup="stopMotion"> Strafe Left </v-btn>
    <v-btn depressed v-on:mousedown="strafe_right" v-on:mouseup="stopMotion"> Strafe Right </v-btn>
    <v-btn depressed v-on:mousedown="forward_left" v-on:mouseup="stopMotion"> Forward Left </v-btn>
    <v-btn depressed v-on:mousedown="forward_right" v-on:mouseup="stopMotion"> Forward Right </v-btn>
    <v-btn depressed v-on:mousedown="backward_left" v-on:mouseup="stopMotion"> Backward Left </v-btn>
    <v-btn depressed v-on:mousedown="backward_right" v-on:mouseup="stopMotion"> Backward Right </v-btn>
    
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
    speed: 512, // Initialize to the required speed
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
    spin_left(){
      console.log("spin_left");
      this.sendCommand("kit._kit.car.spin_left()")
    },
    spin_right(){
      console.log("spin_right");
      this.sendCommand("kit._kit.car.spin_right()")
    },
	strafe_left(){
      console.log("strafe_left");
      this.sendCommand("kit._kit.car.strafe_left()")
    },
    strafe_right(){
      console.log("strafe_right");
      this.sendCommand("kit._kit.car.strafe_right()")
    },
    forward_left(){
      console.log("forward_left");
      this.sendCommand("kit._kit.car.forward_left()")
    },
    forward_right(){
      console.log("forward_right");
      this.sendCommand("kit._kit.car.forward_right()")
    },
    backward_left(){
      console.log("backward_left");
      this.sendCommand("kit._kit.car.backward_left()")
    },
    backward_right(){
      console.log("backward_right");
      this.sendCommand("kit._kit.car.backward_right()")
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
