<template>
    <div id="DemoKit" :style="{'cursor': 'pointer'}">
    <p>DemoKit</p>
  
  
      <!---- Move Buttons ----->
      <v-btn depressed v-on:click="led_blue"> LED BLUE </v-btn>
      <v-btn depressed v-on:click="led_red"> LED RED </v-btn>

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
    }),
  
    mounted(){
      console.log('starting demo kit');
      this.parent.device.rcService.handleResp = this.kitResponseHandler
      this.prepareKit();
    },
  
    methods: {
      kitResponseHandler(resp){
        console.log("kit response " + resp);
      },
  
  
      led_red(){
        console.log("led_red");
        this.sendCommand("kit._kit.led_blue()")
      },
      led_blue(){
        console.log("led_red");
        this.sendCommand("kit._kit.led_red()")
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
  