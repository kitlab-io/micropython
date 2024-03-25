<template>

  <div id="ImuKit" :style="{'cursor': 'pointer'}">
  <p>IMU Kit</p>
  
  <v-btn @click="startImueRead">{{ readImueMsg }}</v-btn>
      
  </div>
</template>

<script>
const startReadImuMsg = "Start IMU Sensing";
const stopReadImuMsg = "Stop IMU Sensing";

module.exports = {
  name: 'ImuKit',
  props: ['parent'],

  data: () => ({
    imu: {'angles': {'roll': 0, 'pitch': 0, 'yaw': 0}, 'accel': {'x': 0, 'y': 0, 'z': 0}},
    resp: "",
    readImueMsg: startReadImueMsg,

  }),

  mounted(){
    console.log('starting demo kit');
    this.parent.device.rcService.handleAuxResp = this.kitAuxRespHandler;
  },

  beforeDestroy() {
      // any code that needs to be stopped before vue file closed can go here
  },

  methods: {

    kitAuxRespHandler(resp){
        console.log("kit aux response " + resp);
        
        let strResp = new TextDecoder().decode(resp);
        this.resp = this.resp.concat(strResp);
        console.log("kit aux str response " + this.resp);
        try
        {
          let jsonStr = JSON.parse(this.resp);
          /* example 
             jsonStr = {"angles": {'roll': -1.75, 'yaw': 359.9375, 'pitch': -5.9375}, 
             "accel": {'x':1.9, 'y':5.81, 'z':9.88}}
          */
          this.imu = jsonStr;
          console.log(jsonStr);
          this.resp = "";  // reset
        }
        catch(e)
        {
          console.warn("kitAuxRespHandler: " + e);
        }
      },
    
    async startImuRead()
    {
      if(this.readImueMsg == startReadImuMsg)
      {
        this.readImueMsg = stopReadImuMsg;
      }
      else 
      {
        this.readImuMsg = startReadImuMsg;
      }
    },
  }
}
</script>
