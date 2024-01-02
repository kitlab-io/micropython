<template>
    <div>
      <button @click="enableStrafe">{{ EnableStrafeMessage }}</button>
    <div :style="joysticksContainerStyle">
      <div :style="topJoysticksStyle">
        <div v-for="index in [0, 1]" :key="index" :style="joystickStyle" ref="joysticks" @mousedown="startTracking(index, $event)" @mouseup="stopTracking(index)" @mousemove="trackMovement(index, $event)" @touchstart="startTracking(index, $event)" @touchmove="trackMovement(index, $event)" @touchend="stopTracking(index)">
          <div :style="outerCircleStyle">
            <div :style="innerCircleStyle(index)"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <script>
  const LeftJoystickIndex = 0;
  const RightJoystickIndex = 1;
  module.exports = {
    name: 'Joystick',
    props: ['parent'],
    data() {
      return {
        EnableStrafeMessage: "Enable Strafe",
        strafeEnabled: false,
        sendControlTimer: null,
        rightIntensity: 0,
        forwardIntensity: 0,
        prevRightIntensity: 0,
        prevForwardIntensity: 0,
        joysticks: [
          { tracking: false, startX: 0, startY: 0, currentX: 0, currentY: 0, prevY: 0, prevX: 0 },
          { tracking: false, startX: 0, startY: 0, currentX: 0, currentY: 0, prevY: 0, prevX: 0 },
        ]
      };
    },
    computed: {
      joysticksContainerStyle() {
        return {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        };
      },
      topJoysticksStyle() {
        return {
          display: 'flex',
          justifyContent: 'space-around',
          width: '100%',
          marginBottom: '15%',
        };
      },
      bottomJoystickStyle() {
        return {
          display: 'flex',
          justifyContent: 'center',
        };
      },
      joystickStyle() {
        return {
          width: '50vmin',
          height: '50vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        };
      },
      outerCircleStyle() {
        return {
          backgroundColor: 'green',
          borderRadius: '50%',
          width: '25vmin',
          height: '25vmin',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        };
      },
      innerCircleStyle() {
        return index => ({
          backgroundColor: 'grey',
          borderRadius: '50%',
          width: '10vmin',
          height: '10vmin',
          transform: `translate(${this.joysticks[index].currentX}px, ${this.joysticks[index].currentY}px)`,
        });
      }
    },
    methods: {
      enableStrafe()
      {
        console.log("Enable Strafe")
        if(this.EnableStrafeMessage == "Enable Strafe")
        {
          this.EnableStrafeMessage = "Disable Strafe"
          this.strafeEnabled = true;
        }
        else 
        {
          this.EnableStrafeMessage = "Enable Strafe"
          this.strafeEnabled = false;
        }
      },

      async startSendControlCmd()
      {
        let frwd = this.forwardIntensity;
        let right = this.rightIntensity;
        if(frwd!= this.prevForwardIntensity || right != this.prevRightIntensity)
        {
            console.log("send f: " + frwd);
            console.log("send r: " + right);
            this.prevRightIntensity = right;
            this.prevForwardIntensity = frwd;
            let cmd = this.controlMotors(frwd, right);//this.controlMotors(frwd, right);
            this.parent.device.send(cmd);
            //this.parent.device.send(`frwd=${frwd};right=${right}\n\r`);
        }
        this.sendControlTimer = setTimeout(() => {this.startSendControlCmd();}, 100);
      },

controlMotors(forwardIntensity, rightIntensity) {
    console.log("strafe: %s, %s" % (forwardIntensity, rightIntensity));
    // Ensure intensities are within the allowed range
    forwardIntensity = Math.max(-100, Math.min(100, forwardIntensity));
    rightIntensity = Math.max(-100, Math.min(100, rightIntensity));
    // Initialize wheel speeds
    let leftWheelSpeed = 0;
    let rightWheelSpeed = 0;

    if (forwardIntensity !== 0 && rightIntensity === 0) {
        // Move forward or backward without turning
        leftWheelSpeed = rightWheelSpeed = forwardIntensity;
    } else if (forwardIntensity === 0 && rightIntensity !== 0) {
        // Turn in place
        leftWheelSpeed = rightIntensity;
        rightWheelSpeed = -rightIntensity;
    } else if (forwardIntensity !== 0 && rightIntensity !== 0) {
        // Move and turn
        leftWheelSpeed = Math.min(100, Math.max(-100, forwardIntensity + rightIntensity));
        rightWheelSpeed = Math.min(100, Math.max(-100, forwardIntensity - rightIntensity));
    }

    // Create the controls object
    let controls = null;
    if(this.strafeEnabled)
    {
      controls = {
          'left_back_motor': forwardIntensity - rightIntensity,
          'right_front_motor': forwardIntensity - rightIntensity,
          'left_front_motor': forwardIntensity + rightIntensity,
          'right_back_motor': forwardIntensity + rightIntensity
      };
    }
    else 
    {
      controls = {
        'left_back_motor': leftWheelSpeed,
        'right_front_motor': rightWheelSpeed,
        'left_front_motor': leftWheelSpeed,
        'right_back_motor': rightWheelSpeed
    };
    }

    let left_back_motor = controls['left_back_motor'] >= 0 ? 0b00010000 : 0b00100000;
    let right_front_motor = controls['right_front_motor'] >= 0  ?  0b00000010 : 0b00000001;
    let left_front_motor = controls['left_front_motor'] >= 0  ? 0b00000100 : 0b00001000;
    let right_back_motor = controls['right_back_motor'] >= 0 ? 0b10000000 : 0b01000000;


    let pwmC = Math.abs(controls['left_back_motor']);//controls['left_back_motor']['speed'];
    let pwmB = Math.abs(controls['right_front_motor']);//controls['right_front_motor']['speed'];
    let pwmA = Math.abs(controls['left_front_motor']);//controls['left_front_motor']['speed'];
    let pwmD = Math.abs(controls['right_back_motor'] );//controls['right_back_motor']['speed'];

    let driverOutput = left_back_motor | right_front_motor | left_front_motor | right_back_motor;

    // Return the controls object
    let cmd = `kit._kit.car.update(${driverOutput}, ${pwmA}, ${pwmB}, ${pwmC}, ${pwmD})\n\r`;
    function dec2bin(dec) {
      return (dec >>> 0).toString(2);
    }
    console.log(dec2bin(driverOutput));
    console.log(cmd);
    return cmd;
},


      getClientPosition(event) {
        if (event.type.startsWith('touch')) {
          return {
            clientX: event.touches[0].clientX,
            clientY: event.touches[0].clientY
          };
        }
        return {
          clientX: event.clientX,
          clientY: event.clientY
        };
      },

      startTracking(index, event) {
        const { clientX, clientY } = this.getClientPosition(event);
        const joystickRef = this.$refs.joysticks[index] || this.$refs.joystick2;
        const rect = joystickRef.getBoundingClientRect();
        this.joysticks[index].startX = clientX;
        this.joysticks[index].startY = clientY;
        this.joysticks[index].tracking = true;
        this.trackMovement(index, event);
      },
      trackMovement(index, event) {
        if (!this.joysticks[index].tracking) return;
        const { clientX, clientY } = this.getClientPosition(event);
        const joystickRef = this.$refs.joysticks[index] || this.$refs.joystick2;
        const rect = joystickRef.getBoundingClientRect();
  
        // Calculate the relative position within the joystick
        let deltaX = clientX - rect.left - rect.width / 2;
        let deltaY = clientY - rect.top - rect.height / 2;
  
        // Apply constraints to keep the inner circle within the joystick bounds
        let maxRadius = rect.width / 2;
        let distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (distance > maxRadius) {
          let angle = Math.atan2(deltaY, deltaX);
          deltaX = Math.cos(angle) * maxRadius;
          deltaY = Math.sin(angle) * maxRadius;
        }
  
        this.joysticks[index].prevX = this.joysticks[index].currentX;
        this.joysticks[index].prevY = this.joysticks[index].currentY;
        this.joysticks[index].currentX = deltaX;
        this.joysticks[index].currentY = deltaY;
        this.updateJoystick(index);
      },
      updateJoystick(index) {

        const joystickRef = this.$refs.joysticks[index];
        let angleRadians = Math.atan2(this.joysticks[index].currentY, this.joysticks[index].currentX);
        let angleDegrees = angleRadians * (180 / Math.PI);
        let adjustedAngle = (360 - angleDegrees) % 360;
        let currentRadius = Math.sqrt(this.joysticks[index].currentX * this.joysticks[index].currentX + this.joysticks[index].currentY * this.joysticks[index].currentY);
        let maxRadius = joystickRef.offsetWidth / 4;
        let radiusRatio = Math.min(currentRadius / maxRadius, 1);
        let radiusPercent = radiusRatio * 100;
        let data = { x: this.joysticks[index].currentX, y: this.joysticks[index].currentY, angle: adjustedAngle, radius: currentRadius};
        let xPercent = parseInt(100 * this.joysticks[index].currentX/maxRadius);
        let yPercent = parseInt(100 * this.joysticks[index].currentY/maxRadius);
        let diffX = Math.abs(parseInt(this.joysticks[index].prevX - this.joysticks[index].currentX));
        let diffY = Math.abs(parseInt(this.joysticks[index].prevY - this.joysticks[index].currentY));
        let changed = false;

        if(diffY && index == LeftJoystickIndex)
        {
            // forward/backward control is left joystick
            changed = true;
            let sign = Math.sign(yPercent);
            this.forwardIntensity = Math.abs(yPercent) >= 100 ? sign * 100 : yPercent; 
            console.log({ x: this.joysticks[index].currentX, max: maxRadius, angle: adjustedAngle, radius: currentRadius, radiusPercent });
        }
        else if(diffX && index == RightJoystickIndex)
        {
            // left/right control is right joystick
            changed = true;
            let sign = Math.sign(xPercent);
            this.rightIntensity = Math.abs(xPercent) >= 100 ? sign * 100 : xPercent; 
            console.log({ x: this.joysticks[index].currentX, max: maxRadius, angle: adjustedAngle, radius: currentRadius, radiusPercent });
        }

        if(changed && this.sendControlTimer == null)
        {
            this.startSendControlCmd();
        }
      },
      stopTracking(index) {
        this.joysticks[index].tracking = false;
        this.joysticks[index].currentX = 0;
        this.joysticks[index].currentY = 0;
        if(index == LeftJoystickIndex)
        {
            this.forwardIntensity = 0; 
        }
        else if(index == RightJoystickIndex)
        {
            this.rightIntensity = 0; 
        }
      }
    }
  };
  </script>
  