# matrix_demo.py
# Modified from: https://github.com/noahwilliamsson/lamatrix/blob/master/main.py
# Modified by: jbthompson.eng@gmail.com
import sys
import time
import gc
from math import ceil
import json
import _thread
from kits.lantern.ledmatrix import LedMatrix
# This is to make sure we have a large contiguous block of RAM on devices with
# 520kB RAM after all modules and modules have been compiled and instantiated.
#
# In the weather scene, the ussl module needs a large chunk of around 1850
# bytes, and without the dummy allocation below the heap will be too
# fragmented after all the initial processing to find such a large chunk.
#large_temp_chunk = bytearray(3400)
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
		self._running = False
		self.render_loop = RenderLoop(self.display, self.config)

	def connect_to_internet(self):
		# This will connect Pycom wifi to internet assumming config.json was setup with ssid / password
		print("Connect to network from spec in config.js")
		wlan = WLAN(mode=WLAN.STA)
		if not wlan.isconnected():
			print('WLAN: Scanning for networks')
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
		if not wlan.isconnected():
			# TODO: This will only use SSID/auth settings from NVRAM during cold boots
			print('WLAN: No known networks')
		else:
			self.display.clear()
			print('WLAN: Connected with IP: {}'.format(wlan.ifconfig()[0]))
			# Initialize RTC now that we're connected
			self.display.set_rtc(scene)

	def start_demo_scene(self):
		if 'Demo' in self.config:
			from kits.demo.demoscene import DemoScene
			scene = DemoScene(self.display, self.config['Demo'])
			self.render_loop.add_scene(scene)
			gc.collect()
			if not self._running:
				self.start_rendering()
		else:
			print("Failed - not included / enabled in config.js")

	def start_clock_scene(self):
		if 'Clock' in self.config:
			from kits.demo.clockscene import ClockScene
			scene = ClockScene(self.display, self.config['Clock'])
			self.render_loop.add_scene(scene)
			gc.collect()
			if not self._running:
				self.start_rendering()
		else:
			print("Failed - not included / enabled in config.js")

	def start_weather_scene(self):
		if 'Weather' in self.config:
			from kits.demo.weatherscene import WeatherScene
			self.connect_to_internet()
			scene = WeatherScene(self.display, self.config['Weather'])
			self.render_loop.add_scene(scene)
			gc.collect()
			if not self._running:
				self.start_rendering()
		else:
			print("Failed - not included / enabled in config.js")

	def start_fire_scene(self):
		if 'Fire' in self.config:
			from kits.demo.firescene import FireScene
			scene = FireScene(self.display, self.config['Fire'])
			self.render_loop.add_scene(scene)
			gc.collect()
			if not self._running:
				self.start_rendering()
		else:
			print("Failed - not included / enabled in config.js")

	def start_animation_scene(self):
		if 'Animation' in self.config:
			from kits.demo.animationscene import AnimationScene
			scene = AnimationScene(self.display, self.config['Animation'])
			self.render_loop.add_scene(scene)
			gc.collect()
			if not self._running:
				self.start_rendering()

		else:
			print("Failed - not included / enabled in config.js")

	def _start_rendering_thread(self):
		print("_start_rendering_thread")
		while self._running:
			self.render_loop.next_frame()

	def start_rendering(self):
		print("start_rendering")
		self._running = True
		_thread.start_new_thread(self._start_rendering_thread, ())

	def stop_rendering(self):
		print("stop_rendering")
		self._running = False

	def clear_all(self):
		if self._running:
			self.stop_rendering()
			time.sleep(1)
		self.render_loop.clear_all()
