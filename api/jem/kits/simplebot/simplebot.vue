<template>
  <div id="SimpleBot" :style="{'cursor': 'pointer'}">
  <p>SimpleBot</p>


    <!---- Move Buttons ----->
    <v-btn depressed v-on:click="forward"> Forward </v-btn>
    <v-btn depressed v-on:click="backward"> Backward </v-btn>
    <v-btn depressed v-on:click="left"> Turn Left </v-btn>
    <v-btn depressed v-on:click="right"> Turn Right </v-btn>

  </div>
</template>

<script>
module.exports = {
  name: 'SimpleBot',
  props: ['parent'],
  components: {
    // GithubCorner
  },
  data: () => ({
    kitReady: false,
  }),

  mounted(){
    console.log('starting simplebot kit');
    this.parent.device.rcService.handleResp = this.kitResponseHandler
    this.prepareKit();
  },

  methods: {
    kitResponseHandler(resp){
      console.log("kit response " + resp);
    },


    forward(){
      console.log("forward");
      this.sendCommand("kit._kit.robot.forward()")
    },
    backward(){
      console.log("backward");
      this.sendCommand("kit._kit.robot.backward()")
    },
    left(){
      console.log("left");
      this.sendCommand("kit._kit.robot.turn_left()")
    },
    right(){
      console.log("right");
      this.sendCommand("kit._kit.robot.turn_right()")
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
