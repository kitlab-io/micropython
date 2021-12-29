# matrix_demo.py
# Modified from: https://github.com/noahwilliamsson/lamatrix/blob/master/main.py
# Modified by: jbthompson.eng@gmail.com
import sys
import time
import gc
from math import ceil
import json
from kits.demo.ledmatrix import LedMatrix
# This is to make sure we have a large contiguous block of RAM on devices with
# 520kB RAM after all modules and modules have been compiled and instantiated.
#
# In the weather scene, the ussl module needs a large chunk of around 1850
# bytes, and without the dummy allocation below the heap will be too
# fragmented after all the initial processing to find such a large chunk.
large_temp_chunk = bytearray(3400)
from network import WLAN
gc.collect()
from kits.demo.renderloop import RenderLoop

class MatrixDemo:
	def __init__(self):
		f = open('/flash/kits/demo/config.json')
		self.config = json.loads(f.read())
		f.close()
    	# Initialize led matrix framebuffer on top of Neopixel -> WS2812 driver
		self.display = LedMatrix(self.config['LedMatrix'])
		self.display.driver.clear_display()
	def start(self):
		# We're running under MCU here
		from kits.demo.bootscene import BootScene
		scene = BootScene(self.display, self.config['Boot'])
		wlan = WLAN(mode=WLAN.STA)
		if not wlan.isconnected():
			print('WLAN: Scanning for networks')
			scene.render(0,0,0)
			default_ssid, default_auth = wlan.ssid(), wlan.auth()
			candidates = wlan.scan()
			for c in candidates:
				print("candidate: %s" % c)

			for conf in self.config['networks']:
				nets = [candidate for candidate in candidates if candidate.ssid == conf['ssid']]
				if not nets:
					continue
				print('WLAN: Connecting to known network: {}'.format(nets[0].ssid))
				wlan.connect(ssid=conf['ssid'], auth=(WLAN.WPA2, conf['password']))
				for i in range(1,40):
					scene.render(i, 0, 0)
					time.sleep(0.2)
					if wlan.isconnected():
						break
				if wlan.isconnected():
					break
		scene.render(0, 0, 0)
		if not wlan.isconnected():
			# TODO: This will only use SSID/auth settings from NVRAM during cold boots
			print('WLAN: No known networks')
		else:
			self.display.clear()
			print('WLAN: Connected with IP: {}'.format(wlan.ifconfig()[0]))
			# Initialize RTC now that we're connected
			self.display.set_rtc(scene)
			scene.render(0,0,0)
		scene = None
		del BootScene


		# This is where it all begins
		r = RenderLoop(self.display, self.config)

		if 'Demo' in self.config:
			from kits.demo.demoscene import DemoScene
			scene = DemoScene(self.display, self.config['Demo'])
			r.add_scene(scene)
			gc.collect()
			
		if 'Clock' in self.config:
			from kits.demo.clockscene import ClockScene
			scene = ClockScene(self.display, self.config['Clock'])
			r.add_scene(scene)
			gc.collect()

		if 'Weather' in self.config:
			from kits.demo.weatherscene import WeatherScene
			scene = WeatherScene(self.display, self.config['Weather'])
			r.add_scene(scene)
			gc.collect()

		if 'Fire' in self.config:
			from kits.demo.firescene import FireScene
			scene = FireScene(self.display, self.config['Fire'])
			r.add_scene(scene)
			gc.collect()

		if 'Animation' in self.config:
			from kits.demo.animationscene import AnimationScene
			scene = AnimationScene(self.display, self.config['Animation'])
			r.add_scene(scene)
			gc.collect()

		# Now that we're all setup, release the large chunk
		large_temp_chunk = None

		# Render scenes forever
		while True:
			r.next_frame(0)
