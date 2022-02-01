# The game looop
import time
import gc
from math import ceil

class RenderLoop:
	def __init__(self, display, config=None):
		self.display = display
		self.debug = False
		self.fps = display.fps
		self.display.clear()
		self.config = config
		self.clear_all()
		if self.config and 'debug' in self.config:
			self.debug = self.config['debug']

	def clear_all(self):
		self.t_next_frame = None
		self.prev_frame = 0
		self.frame = 1
		self.t_init = time.ticks_ms()
		self.scenes = []
		self.scene_index = 0
		self.scene_switch_countdown = self.fps * 40
		self.scene_switch_effect = 0
		if self.config and 'sceneTimeout' in self.config:
			print("sceneTimeout = %s" % self.config['sceneTimeout'])
			self.scene_switch_countdown = self.fps * self.config['sceneTimeout']

	def add_scene(self, scene):
		"""
		Add new scene to the render loop.
		Called by main.py.
		"""
		print("add_scene: %s" % scene)
		self.scenes.append(scene)

	def next_frame(self):
		"""
		Display next frame, possibly after a delay to ensure we meet the FPS target
		Called by main.py.
		"""

		scene = self.scenes[self.scene_index]
		# Calculate how much we need to wait before rendering the next frame
		t_now = time.ticks_ms() - self.t_init
		if not self.t_next_frame:
			self.t_next_frame = t_now

		delay = self.t_next_frame - t_now
		if delay >= 0:
			# Wait until we can display next frame
			time.sleep_ms(delay)
		else:
			# Resynchronize
			num_dropped_frames = ceil(-delay*self.fps/1000)
			if self.debug:
				print('RenderLoop: FPS {} too high, should\'ve rendered frame {} at {}ms but was {}ms late and dropped {} frames'.format(self.fps, self.frame, self.t_next_frame, -delay, num_dropped_frames))
			self.frame += num_dropped_frames
			self.t_next_frame += ceil(1000*num_dropped_frames/self.fps)
			if self.debug:
				print('RenderLoop: Updated frame counters to frame {} with current next at {}'.format(self.frame, self.t_next_frame))

		# Let the scene render its frame
		t = time.ticks_ms()
		loop_again = scene.render(self.frame, self.frame - self.prev_frame - 1, self.fps)
		t = time.ticks_ms() - t
		if t > 1000/self.fps and self.debug:
			print('RenderLoop: WARN: Spent {}ms rendering'.format(t))


		# Consider switching scenes and update frame counters
		self.scene_switch_countdown -= 1
		scene_increment = 1
		if not loop_again:
			self.scene_switch_countdown = 0

		if not self.scene_switch_countdown:
			self.reset_scene_switch_counter()
			# Transition to next scene
			self.next_scene(scene_increment)
			# Account for time wasted above
			t_new = time.ticks_ms() - self.t_init
			t_diff = t_new - t_now
			frames_wasted = ceil(t_diff*self.fps/1000.0)
			if self.debug:
				print('RenderLoop: setup: scene switch took {}ms, original t {}ms, new t {}ms, spent {} frames'.format(t_diff, t_now,t_new, self.fps*t_diff/1000.0))
			self.frame += int(frames_wasted)
			self.t_next_frame += int(1000.0 * frames_wasted / self.fps)

		self.prev_frame = self.frame
		self.frame += 1
		self.t_next_frame += int(1000/self.fps)

	def reset_scene_switch_counter(self):
		"""
		Reset counter used to automatically switch scenes.
		The counter is decreased in .next_frame()
		"""
		self.scene_switch_countdown = 45 * self.fps

	def next_scene(self, increment=1):
		"""
		Transition to a new scene and re-initialize the scene
		"""
		if len(self.scenes) < 2:
			return

		print('RenderLoop: next_scene: transitioning scene')
		# Fade out current scene
		t0 = time.ticks_ms()

		effect = self.scene_switch_effect
		self.scene_switch_effect = (effect + 1) % 4
		if effect == 0:
			self.display.vscroll()
		elif effect == 1:
			self.display.hscroll()
		elif effect == 2:
			self.display.fade()
		else:
			self.display.dissolve()

		t2 = time.ticks_ms()
		t1 = t2 - t0
		gc.collect()

		t3 = time.ticks_ms()
		t2 = t3 - t1
		num_scenes = len(self.scenes)
		i = self.scene_index = (num_scenes + self.scene_index + increment) % num_scenes
		# (Re-)initialize scene
		self.scenes[i].reset()
		t4 = time.ticks_ms()
		t3 = t4 - t3
		if self.debug:
			print('RenderLoop: next_scene: selected {}, effect {}ms, gc {}ms, scene reset {}ms, total {}ms'.format(self.scenes[i].__class__.__name__, t1, t2, t3, t4-t0))
		return
