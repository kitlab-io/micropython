# matrix_demo.py
# Modified from: https://github.com/noahwilliamsson/lamatrix/blob/master/main.py
# Modified by: jbthompson.eng@gmail.com
import sys
import time
import gc
from math import ceil
import ujson as json
from ledmatrix import LedMatrix
# This is to make sure we have a large contiguous block of RAM on devices with
# 520kB RAM after all modules and modules have been compiled and instantiated.
#
# In the weather scene, the ussl module needs a large chunk of around 1850
# bytes, and without the dummy allocation below the heap will be too
# fragmented after all the initial processing to find such a large chunk.
large_temp_chunk = bytearray(3400)
from network import WLAN
gc.collect()
from renderloop import RenderLoop

def sigint_handler(sig, frame):
	"""
	Clear display when the program is terminated by Ctrl-C or SIGTERM
	"""
	global display
	display.driver.clear_display()
	sys.exit(0)


if __name__ == '__main__':
	f = open('config.json')
	config = json.loads(f.read())
	f.close()
	del json

    # Initialize led matrix framebuffer on top of Neopixel -> WS2812 driver
	display = LedMatrix(config['LedMatrix'])
	display.driver.clear_display()

	# We're running under MCU here
	from bootscene import BootScene
	scene = BootScene(display, config['Boot'])
	wlan = WLAN(mode=WLAN.STA)
	if not wlan.isconnected():
		print('WLAN: Scanning for networks')
		scene.render(0,0,0)
		default_ssid, default_auth = wlan.ssid(), wlan.auth()
		candidates = wlan.scan()
		for conf in config['networks']:
			nets = [candidate for candidate in candidates if candidate.ssid == conf['ssid']]
			if not nets:
				continue
			print('WLAN: Connecting to known network: {}'.format(nets[0].ssid))
			wlan.connect(nets[0].ssid, auth=(nets[0].sec, conf['password']))
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
		print('WLAN: No known networks, enabling AP with ssid={}, pwd={}'.format(default_ssid, default_auth[1]))
		wlan.init(mode=WLAN.AP, ssid=default_ssid, auth=default_auth, channel=6)
	else:
		display.clear()
		print('WLAN: Connected with IP: {}'.format(wlan.ifconfig()[0]))
		# Initialize RTC now that we're connected
		display.set_rtc(scene)
		scene.render(0,0,0)
	scene = None
	del BootScene


	# This is where it all begins
	r = RenderLoop(display, config)

	if 'Clock' in config:
		from clockscene import ClockScene
		scene = ClockScene(display, config['Clock'])
		r.add_scene(scene)
		gc.collect()

	if 'Demo' in config:
		from demoscene import DemoScene
		scene = DemoScene(display, config['Demo'])
		r.add_scene(scene)
		gc.collect()

	if 'Weather' in config:
		from weatherscene import WeatherScene
		scene = WeatherScene(display, config['Weather'])
		r.add_scene(scene)
		gc.collect()

	if 'Fire' in config:
		from firescene import FireScene
		scene = FireScene(display, config['Fire'])
		r.add_scene(scene)
		gc.collect()

	if 'Animation' in config:
		from animationscene import AnimationScene
		scene = AnimationScene(display, config['Animation'])
		r.add_scene(scene)
		gc.collect()

	# Now that we're all setup, release the large chunk
	large_temp_chunk = None

	# Render scenes forever
	while True:
		r.next_frame(0)
