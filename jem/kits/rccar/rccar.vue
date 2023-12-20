<template>
    <div :style="joystickStyle" @mousedown="startTracking" @mouseup="stopTracking" @mouseleave="stopTracking" @mousemove="trackMovement" @touchstart="startTracking" @touchmove="trackMovement" @touchend="stopTracking">
        <div :style="outerCircleStyle">
        <div :style="innerCircleStyle"></div>
      </div>
    </div>
  </template>
  
  <script>
  module.exports = {
    name: 'RCcar',
    props: ['parent'],
    data() {
      return {
        tracking: false,
        startX: 0,
        startY: 0,
        currentX: 0,
        currentY: 0,
        prevCmd: null,
        prevIntensity: null,
        sendTimer: null,
        controlCmd: "kit._kit.car.stop()"
      };
    },
    computed: {
      joystickStyle() {
        return {
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '50vmin',
          height: '50vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        };
      },
      outerCircleStyle() {
        return {
          backgroundColor: 'orange',
          borderRadius: '50%',
          width: '25vmin',
          height: '25vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        };
      },
      innerCircleStyle() {
        return {
          backgroundColor: 'darkorange',
          borderRadius: '50%',
          width: '10vmin',
          height: '10vmin',
          transform: `translate(${this.currentX}px, ${this.currentY}px)`
        };
      }
    },
    methods: {
        sendCommand(cmdStr){
            console.log(cmdStr);
            return this.parent.device.send(cmdStr); //this.parent.device.rcService.sendCommand(cmdStr);
        },
        
        startTracking(event) {
            this.tracking = true;
            const rect = this.$el.getBoundingClientRect();
            this.startX = rect.left + rect.width / 2;
            this.startY = rect.top + rect.height / 2;
            this.trackMovement(event);
        },

        trackMovement(event) {
            if (!this.tracking) return;
            let x = (event.clientX || event.touches[0].clientX) - this.startX;
            let y = (event.clientY || event.touches[0].clientY) - this.startY;
            this.currentX = x;
            this.currentY = y;

            // Calculate angle in radians, then convert to degrees
            let angleRadians = Math.atan2(y, x);
            let angleDegrees = angleRadians * (180 / Math.PI);

            // Reverse the direction (counterclockwise) and ensure the angle is within 0-360 degrees
            let adjustedAngle = (360 - angleDegrees) % 360;

            let currentRadius = Math.sqrt(x * x + y * y);
            let maxRadius = this.$el.offsetWidth / 2; // The radius of the outer circle
            let radiusRatio = Math.min(currentRadius / maxRadius, 1); // Ratio, capped at 1 (100%)
            let radiusPercent = radiusRatio * 100; // Convert to percentage

            let angle = adjustedAngle;

            console.log('joystick-move')
            console.log( { x, y, angle, currentRadius, radiusPercent, maxRadius });
            let cmd = "stop()";
            if(angle <= 22.5 || angle >= 337.5)
            {
                angle = 0 // strafe right
                console.log(angle);
                cmd = "strafe_right()";
            }
            else if(angle > 22.5 && angle < 67.5)
            {
                angle = 45; //forward right
                cmd = "forward_right()";
                console.log(angle);
            }
            else if(angle >= 67.5 && angle < 112.5)
            {
                angle = 90; //forward
                console.log(angle);
                cmd = "forward()";
            }
            else if(angle >= 112.5 && angle < 157.5)
            {
                angle = 135; // forward left
                console.log(angle);
                cmd = "forward_left()";
            }
            else if(angle >= 157.5 && angle < 202.5)
            {
                angle = 180; // strafe left
                console.log(angle);
                cmd = "strafe_left()";
            }
            else if(angle >= 202.5 && angle < 247.5)
            {
                angle = 225; // backward left
                console.log(angle);
                cmd = "backward_left()";
            }
            else if(angle >= 247.5 && angle < 292.5)
            {
                angle = 270; // backwards
                console.log(angle);
                cmd = "backwards()";
            }
            else if(angle >= 292.5 && angle < 337.5)
            {
                angle = 315; // backwards right
                console.log(angle);
                cmd = "backward_left()";
            }
            else 
            {
                console.log("woops");
                cmd = "stop()";
            }
            let intensity = parseInt(radiusPercent); //ex 0 - 100% to control motor intensity
            console.log("cmd: " + cmd);
			let dirCmd = null;
            let intensityCmd = null;
            
            if(this.prevIntensity != intensity)
            {
                this.prevIntensity = intensity;
                console.log("sendIntensity: " + intensity);
                if(intensity > 100)
                {
                    intensity = 100;
                }
                let pwmVal = intensity * 800/100; // max 800 since at 1023 motor starts to strain
                intensityCmd = `kit._kit.car.set_speed(${pwmVal})`
                this.controlCmd = intensityCmd + ";";
            }
            if(this.prevCmd != cmd)
            {
                console.log("sendDir: " + cmd);
                this.prevCmd = cmd;
                dirCmd = "kit._kit.car." + cmd; //ex: kit._kit.car.forward()
                if(intensityCmd)
                {
                	this.controlCmd += dirCmd; //ex: kit._kit.car.set_speed(10);kit._kit.car.stop()
                }
                else 
                {
                  this.controlCmd = dirCmd;
                }
            }
          	
            if((intensityCmd || dirCmd) && this.sendTimer == null)
            {
              console.log("sendTimer: " + this.sendTimer);
              this.sendTimer = setTimeout(()=>{
                this.sendCommand(this.controlCmd).then(() => {this.sendTimer = null;});
                
              }, 10);
              
            }

        },
        stopTracking() {
          this.tracking = false;
          this.currentX = 0;
          this.currentY = 0;
          console.log("stop car");
          let stopCmd = "kit._kit.car.stop()\n\r";
          if(this.sendTimer)
          {
              clearTimeout(this.sendTimer);
          }
          this.sendTimer = setTimeout(()=>{
            this.sendCommand(stopCmd).then(() => {this.sendTimer = null;});
          }, 10);
        }
    }
  };
  </script>
  