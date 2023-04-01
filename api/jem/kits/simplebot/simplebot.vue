<template>
  <div id="SimpleBot" :style="{'cursor': 'pointer'}">
  <p>SimpleBot</p>

    <!---- Move Buttons ----->
    <v-btn depressed v-on:click="startMotion"> StartMotion </v-btn>
    <v-btn depressed v-on:click="stopMotion"> StopMotion </v-btn>
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
    // motion plugin support
    prevAccelTimeMs: 0,
    accelIntervalMs: 200,
    currentAccelTimsMs: 0,
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

    startMotion(){
      console.log("kit startMotion");
      this.sendCommand("kit._kit.robot.start()");
      this.parent.startMotion(this.motionHandler);
    },

    stopMotion(){
      console.log("kit stopMotion");
      this.sendCommand("kit._kit.robot.stop()");
      this.parent.stopMotion();
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

    motionHandler: function(accelEvent){
        let g_scale = 9.81; // gravity = 9.81 m/s^2
        let x = accelEvent.accelerationIncludingGravity.x; //ex: 9.81
        let y = accelEvent.accelerationIncludingGravity.y;
        this.currentAccelTimsMs += accelEvent.interval*1000; //interval is something like 16 ms
        let elapsedMs = this.currentAccelTimsMs - this.prevAccelTimeMs; //ms

        if(elapsedMs < this.accelIntervalMs) //only handle 200 ms period
        {
          return;
        }
        this.prevAccelTimeMs = this.currentAccelTimsMs; //set new prev time for next successful interval

        if(x > g_scale) {
            x = g_scale;
        }
        else if (x < -1*g_scale) {
            x = -1*g_scale;
        }

        if(y > g_scale){
            y = g_scale;
        }
        else if(y < -1*g_scale) {
            y = -1*g_scale;
        }

        var y_speed = y * (100/g_scale); //ex: 9.81 = 100 %, 0 = 0%
        var x_speed = x * (100/g_scale);

        // add the forward motion
        var speed_left = x_speed
        var speed_right = x_speed


        // add the turn motion component (50% only)
        speed_left += y_speed/2
        speed_right += (-1*y_speed/2)

        if(Math.abs(speed_left) <= 10)
        {
          speed_left = 0;
        }

        if(Math.abs(speed_right) <= 10)
        {
          speed_right = 0;
        }

        let cmdStr = String(`kit._kit.robot.move(left_speed=${speed_left}, right_speed=${speed_right})`)
        this.sendCommand(cmdStr); //send data to JEM
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
