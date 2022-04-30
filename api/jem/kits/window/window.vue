<template>
  <div id="remote-control-window">
    <div class="layout wrap-row mt">
      <section class="nes-container with-title h-container section-paint">
        <!-- <h2 class="title">Paint</h2> -->
        <div class="layout align-end is-paint mt-negative-container">
          <div id="pixel-editor">
            <div class="draw" :style="getDrawStyle" ref="drawGrid">
            <!--<div>1</div><div>2</div><div>3</div><div>4</div><div>5</div><div>6</div><div>7</div><div>8</div>-->
            </div>
          </div>
        </div>

        <div class="nes-field mt">
          <div class="layout nowrap-row align-end pl-field mt-negative">
            <div class="layout nowrap-column nes-field pr-field">
              <label for="color">Brush</label>
              <input
                v-model="color"
                class="nes-input color"
                type="text"
                :style="{ backgroundColor: color }"
                @click="$refs.colorPicker.click()"
                @blur="fillColor"
              />
              <input
                @input="updateColor"
                ref="colorPicker"
                type="color"
                style="display: none"
              />
            </div>
            <div class="layout nowrap-column nes-field">
              <label for="color">Canvas</label>
              <input
                v-model="backgroundColor"
                class="nes-input"
                type="text"
                :style="{ backgroundColor }"
                @input="checkDefault"
                @click="$refs.bgColorPicker.click()"
              />
              <input
                @input="updateBgColor"
                ref="bgColorPicker"
                type="color"
                style="display: none"
              />
            </div>

          </div>

           <div class="layout nowrap-row align-end pl-field mt-negative">
            <div class="layout nowrap-column nes-field pr-field">
          <div class="nes-field mr-field">
            <button class="nes-btn is-error" @click="changeSize">Clear All</button>
          </div>
            </div>
           </div>
        </div>
      </section>

      <footer class="layout justify-center align-center wrap-column">
        <div class="is-canvas">
          <canvas id="canvas" class="canvas" ref="canvas"></canvas>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
const CODE_START = 'no pixel data'

module.exports = {
  name: 'window-kit',
  props: ['parent', 'response', 'auxResponse'],
  components: {
    // GithubCorner
  },
  data: () => ({
    size: 8,
    pixel: 4,
    show: false,
    sizeError: false,
    isMouseDown: false,
    color: '#1cb785',
    code: CODE_START,
    erase: false,
    borders: true,
    downloading: false,
    white: false,
    backgroundColor: '#ffffff',
    colorCache: null,
    kitReady: false
  }),
  computed: {
    getDrawStyle () {
      const { white } = this

      return white ? 'background:#fff !important;' : ''
    }
  },
  created () {
    this.colorCache = new Set()
    this.fillColor()
  },
  mounted () {
    this.changeSize()

    document.addEventListener('mouseup', (el) => {
      if (el && el.target && el.target.parentNode && el.target.parentNode.className !== 'draw') {
        this.isMouseDown = false
      }
    })
  },
  beforeDestroy () {
    this.removeChilds()
    document
      .removeEventListener('mouseup', () => ({}))
  },
  methods: {
    prepareKit(){
      //disable any leds examples running on kit (like button triggered led thread)
      console.log("prepareKit!!!!")
      this.parent.device.rcService.sendCommand("kit._run = False");
    },

    clearDisplay(){
        //clear_display
        if(this.parent.device.isConnected()){
          this.parent.device.rcService.sendCommand(`kit.neopixel.clear_display()`);
        }
    },

    sendPixel(id, rgb_color){
      //id = pixel number on grid (ex: 0)
      //rgb_color = [0, 0, 0] for OFF or you can send actual color like [12, 45, 39]
      //Only send if color changed
      if(this.prev_id == id){
        if(this.prev_rgb_color && this.prev_rgb_color[0] == rgb_color[0] && this.prev_rgb_color[1] == rgb_color[1] && this.prev_rgb_color[2] == rgb_color[2]){
          return;
        }
        else{
          this.prev_rgb_color = rgb_color;
        }
      }
      else{
        this.prev_id = id;
      }
      console.log("sendPixel: " + parseInt(id));
      //console.log(rgb_color);
      //TODO: send color to JEM over ble
      if(this.parent.device.isConnected()){
        if(!this.kitReady){
          this.prepareKit();
          this.kitReady = true;
        }

        let r = parseInt(rgb_color[0]);
        let g = parseInt(rgb_color[1]);
        let b = parseInt(rgb_color[2]);
        let hexColor = this.rgbToHex(r, g, b); //ex: [1,2,3] => '0x010203'
        //this.parent.device.rcService.sendCommand(`kit.jem.led.set_color(${hexColor})`); //ex: set_color(0x110022)       
        this.parent.device.rcService.sendCommand(`kit.neopixel.set_pixel(${id}, (${r}, ${g}, ${b}))`);
      }else {
        console.warn("sendPixel ignored - Device not connected");
      }
    },

    fillColor () {
      this.colorCache.add(this.hexToRgb(this.color))
    },
    togglePaintErase () {
      this.erase = !this.erase
    },
    getAllDivs () {
      const refs = this.$refs
      const grid = refs.drawGrid

      return grid.querySelectorAll('div')
    },
    toggleBorders () {
      const allDivs = this.getAllDivs()

      Array.from(allDivs).forEach(el => {
        el.className = el.className ? '' : 'no-border'
      })
    },
    updateColor (e) {
      const value = e.target.value
      this.color = value
    },
    updateBgColor (e) {
      const value = e.target.value
      this.backgroundColor = value
      this.toggleBgColor()
    },
    toggleBgColor () {
      const allDivs = this.getAllDivs()

      Array.from(allDivs).forEach(el => {
        if (!this.colorCache.has(el.style.backgroundColor)) {
          el.style.backgroundColor = this.backgroundColor
        }
      })
    },
    checkDefault () {
      if (this.backgroundColor === 'default' || !this.backgroundColor) {
        this.backgroundColor = ''
      }

      this.toggleBgColor()
    },
    removeChild (el) {
      el.removeEventListener('click', this
        .paint
        .bind(this, el))
      el.removeEventListener('mousedown', this
        .mousedown
        .bind(this, el))
      el.removeEventListener('mouseup', this
        .mouseup
        .bind(this, el))
      el.removeEventListener('mousemove', this
        .mousemove
        .bind(this, el))
      el
        .parentElement
        .removeChild(el)
    },
    removeChilds () {
      const allDivs = this.getAllDivs()

      Array.from(allDivs).forEach(el => {
        this.removeChild(el)
      })
    },
    resetEventListner () {
      const allDivs = this.getAllDivs()

      Array.from(allDivs).forEach(el => {
        el.addEventListener('mousedown', this
          .mousedown
          .bind(this, el))
        el.addEventListener('mouseup', this
          .mouseup
          .bind(this, el))
        el.addEventListener('mousemove', this
          .mousemove
          .bind(this, el))
        el.addEventListener('click', this
          .paint
          .bind(this, el))
      })
    },

    componentToHex(c) {
      var hex = c.toString(16);
      return hex.length == 1 ? "0" + hex : hex;
    },

    rgbToHex(r, g, b) {
      return "0x" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
    },

    hexToRgb (hex) {
      const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i
      hex = hex.replace(shorthandRegex, function (m, r, g, b) {
        return r + r + g + g + b + b
      })

      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)

      return result
        ? `rgb(${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)})`
        : null
    },
    mousemove (el) {
      if (this.isMouseDown) {
        this.mustPaint(el)
      }
    },
    mousedown (el) {
      this.isMouseDown = true
    },
    mouseup (el) {
      this.isMouseDown = false
    },
    mustPaint (el) {
      this.setBgColor(el, this.erase ? 'transparent' : this.color)
    },
    paint (el) {
      const style = el.style
      const setBackgroundColor = style.backgroundColor === this.hexToRgb(this.color)
        ? 'transparent'
        : this.color

      this.setBgColor(el, setBackgroundColor)
    },
    setBgColor (el, color) {
      el.style.backgroundColor = color
      let pixel_id_str = el.id.split("_")[1];
      const regexpNumbers = /([0-9]+)/g;
      let colorData = el.style.backgroundColor;
      const match = colorData.match(regexpNumbers);
      let pixel = {id: pixel_id_str, color: [0, 0, 0]}
      if(match){
        pixel.color[0] = match[0]; //r
        pixel.color[1] = match[1]; //b
        pixel.color[2] = match[2]; //g
      }
      this.sendPixel(pixel.id, pixel.color);
      //this.output()
    },
    getPixelData () {
      const pixel = 1
      const allDivs = this.getAllDivs()
      const size = parseInt(this.size, 10)
      const pixelData = Array.from(allDivs)
        .map((el, i) => {
          let cellData = [
            `${pixel * (i % size)}`, // col
            `${pixel * Math.ceil((i) / size)}`, // row
            el.style.backgroundColor || null
          ]
          
          const colorData = cellData[2];

          if (colorData != null) {
            console.log("color: " + colorData);
            const regexpNumbers = /([0-9]+)/g;
            const match = colorData.match(regexpNumbers);
            if(match){
              cellData[2] = [match[0], match[1], match[2]]
              console.log("cell data: %d,%d,%d",  cellData[2][0], cellData[2][1], cellData[2][2]);
            }
            else {
              console.log("no match!");
            }
          }
          

          return cellData
        })
      return pixelData
    },
    getBoxShadows (pixel) {
      const allDivs = this.getAllDivs()
      const size = parseInt(this.size, 10)
      const boxShadows = Array.from(allDivs)
        .map((el, i) => {
          return [
            `${pixel * (i % size) + pixel}px`, // col
            `${pixel * Math.ceil((i + 1) / size)}px`, // row
            0,
            el
              .style
              .backgroundColor || 'transparent'
          ].join(' ')
        })

      const spliced = boxShadows.filter(it => !/(\s0 transparent$)/.test(it))

      return spliced.join(', \n')
    },
    output () {
      const pixelData = this.getPixelData()
      this.code = ` ${pixelData}`
    },
    changeSize () {
      const refs = this.$refs
      if (this.size > 100) {
        this.sizeError = true
        return
      }

      this.sizeError = false
      this.borders = true
      const grid = refs.drawGrid
      const length = parseInt(this.size ** 2, 10)
      const qtdDivs = Array(length).fill(0)

      this.code = CODE_START
      //this.removeChilds()
      /*
      let id_list = [7,   6,   5,  4,  3,  2,  1,  0,
                     8,   9,   10, 11, 12, 13, 14, 15,
                     23,  22,  21, 20, 19, 18, 17, 16,
                     24,  25,  26, 27, 28, 29, 30, 31,
                     39,  38,  37, 36, 35, 34, 33, 32,
                     40,  41,  42, 43, 44, 45, 46, 47,
                     55,  54,  53, 52, 51, 50, 49, 48,
                     56,  57,  58, 59, 60, 61, 62, 63];
      */

      let id_list = [0,   1,   2,  3,  4,  5,  6,  7,
                     8,   9,   10, 11, 12, 13, 14, 15,
                     16,  17,  18, 19, 20, 21, 22, 23,
                     24,  25,  26, 27, 28, 29, 30, 31,
                     32,  33,  34, 35, 36, 37, 38, 39,
                     40,  41,  42, 43, 44, 45, 46, 47,
                     48,  49,  50, 51, 52, 53, 54, 55,
                     56,  57,  58, 59, 60, 61, 62, 63];
      for(let i = 0; i<length; i++){
        const div = document.createElement('div')
        let id = id_list[i];
        
        div.setAttribute("id", "pixel_" + id); //can use pixel number to send only one pixel change instead of entire array
        grid.appendChild(div)
      }
      this.clearDisplay();

      this.resetEventListner()

      grid.style.gridTemplateColumns = '1fr '.repeat(this.size);
      grid.style.gridTemplateRows = '1fr '.repeat(this.size);

    },
    onCopy () {
      this.show = true
      setTimeout(() => {
        this.show = false
      }, 2000)
    }
  }
}
</script>

<style>
html, body {
  height: calc(100% - 4.5em);
  width: 100%;
}

a, a:hover {
  text-decoration: none !important;
}

.draw div {
  border: 1px solid #b6b6b6;
  background-color: transparent;
}

.draw .no-border {
  border: 0;
  background-color: transparent;
}
</style>

<style lang="scss">
@import 'nes.scss';
$px: 2px;

#remote-control-window {
  grid-template:
    "editor settings"
    "editor output"
    / auto 400px;
  font-family: 'Press Start 2P', -apple-system, BlinkMacSystemFont, Segoe UI,
    Roboto, Oxygen, Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue,
    sans-serif;
  height: 500%;
  width: 500%;
}

.copied {
  position: absolute !important;
  top: -55px !important;
  left: 30% !important;
}

.before {
  box-sizing: border-box;
  position: relative;
}

.transition {
  transition: .3s all linear !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .8s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.relative {
  position: relative;
}

.hide {
  display: none;
}

.pr-field {
  padding-right: 20px;
}

.pl-field {
  padding-left: 25px;
}

.pr-field-double {
  padding-right: 40px;
}

.mr-field {
  padding-right: 14px;
}

.mt {
  margin-top: $px * 16;
}

.mb {
  margin-bottom: $px * 16;
}

.bgcolor {
  background-image: linear-gradient(45deg, #e2e2e2 25%, transparent 25%, transparent 75%, #e2e2e2 75%, #e2e2e2),
    linear-gradient( 45deg, #e2e2e2 25%, transparent 25%, transparent 75%, #e2e2e2 75%, #e2e2e2);
}

footer .mt {
  margin-top: $px * 11;
}

footer .mb {
  margin-bottom: $px * 11;
}

.pl {
  padding-left: $px * 5;
}

.pr {
  padding-right: $px * 5;
}

.w100px {
  width: 100px;
}

.w30 {
  width: 30%;
}

.w40 {
  width: 40%;
}

.w50 {
  width: 50%;
}

.w60 {
  width: 60%;
}

.w70 {
  width: 70%;
}

.h100 {
  height: 100%;
}

.w33 {
  width: 33%;
}

.btn {
  margin: 0 !important;
  margin-bottom: 2px !important;
}

.input {
  padding: 0.55rem 1rem !important;
}

.h-container {
  height: calc(100% - 10em);

  @media screen and (max-width: 1366px) {
    height: 100%;
  }
}

#pixel-editor {
  grid-area: editor;

  .draw {
    display: grid;
    margin: auto;
    width: 300px;
    height: 300px;
    // width: 600px;
    // height: 600px;
    border: 3px solid #920b0b;
    background-color: #272c77;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    grid-template-rows: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    background-image: linear-gradient(45deg, #e2e2e2 25%, transparent 25%, transparent 75%, #e2e2e2 75%, #e2e2e2),
      linear-gradient( 45deg, #e2e2e2 25%, transparent 25%, transparent 75%, #e2e2e2 75%, #e2e2e2);
    background-size: 30px 30px;
    background-position: 0 0, 15px 15px;
    z-index: 10;
  }
}

@media screen and (max-width: 1366px) {
  .section-paint {
    width: 99.5%;
    margin-left: .3%;
    height: calc(100% - 5em);
    @media screen and (max-height: 769px) and (max-width: 1366px) {
      height: calc(100% + 2em);
    }
  }
  .section-config {
    width: 99.5%;
    margin-left: .3%;
    margin-top: 1em;
    margin-bottom: 1em;
    height: calc(100% - 7em);
    @media screen and (max-height: 769px) {
      height: 100%;
    }
  }
  footer {
    margin-bottom: 1em;
  }
}

@media screen and (min-width: 1367px) and (max-width: 1748px) {
  .is-paint {
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  .section-paint, .section-config {
    height: calc(100% + 10em);

    @media screen and (max-height: 769px) {
      height: calc(100% + 17em);
    }
  }
  .section-config {
    margin-bottom: 1em;
  }
  footer {
    margin-bottom: 1em;
  }
}

@media screen and (min-width: 1367px) and (max-width: 1508px) {
  .is-size, .is-pixels {
    margin-top: 1em;
  }
}

@media screen and (min-width: 1367px) and (max-width: 1847px) {
  .is-pixels {
    margin-top: 1em;
  }
  .section-paint, .section-config {
    width: 49.7%;
    margin-left: .2%;
  }
}

@media screen and (min-width: 1749px) {
  .section-paint, .section-config {
    height: calc(100% - 10em);
    margin-bottom: 1em;
    width: 49.7%;
    margin-left: .2%;

    @media screen and (max-height: 769px) {
      height: calc(100% + 6em);
    }
  }
  footer {
    margin-bottom: 1em;
  }
}

input[type="file"], .is-canvas {
  position: absolute;
  top: -2000px;
  z-index: -1;
  left: 0;
}

.mt-negative {
  margin-top: -15px;
}

.f-size-btns {
  font-size: .9em;
  display: flex;
  justify-content: center;
}

.pl-nes {
  padding-left: 15px;
}

.mt-negative-container {
  margin-top: -2%;
}

</style>
