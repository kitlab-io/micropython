<template>
  <div id="RCcar" :style="{'cursor': 'pointer'}">
  <p>SimpleBot</p>

    <!---- Move Buttons ----->
    <v-btn depressed v-on:click="stopMotion"> StopMotion </v-btn>
    <v-btn depressed v-on:mousedown="forward" v-on:mouseup="stopMotion"> Forward </v-btn>
    <v-btn depressed v-on:mousedown="backward" v-on:mouseup="stopMotion"> Backward </v-btn>
    <v-btn depressed v-on:mousedown="left" v-on:mouseup="stopMotion"> Turn Left </v-btn>
    <v-btn depressed v-on:mousedown="right" v-on:mouseup="stopMotion"> Turn Right </v-btn>

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
  }),

  mounted(){
    console.log('starting RCcar kit');
    this.parent.device.rcService.handleResp = this.kitResponseHandler
    this.prepareKit();
  },

  methods: {
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
