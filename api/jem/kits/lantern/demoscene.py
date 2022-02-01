from kits.lantern.pixelfont import PixelFont

class DemoScene:
	"""This module implements an example scene with a traveling pixel"""

	def __init__(self, display, config):
		"""
		Initialize the module.
		`display` is saved as an instance variable because it is needed to
		update the display via self.display.put_pixel() and .render()
		"""
		self.display = display
		self.intensity = 255
		self.x_pos = 0
		self.text = 'example'
		if not config:
			return
		if 'intensity' in config:
			self.intensity = int(round(config['intensity']*255))

	def reset(self):
		"""
		This method is called before transitioning to this scene.
		Use it to (re-)initialize any state necessary for your scene.
		"""
		self.x_pos = 0
		print('DemoScene: here we go')

	def input(self, button_state):
		"""
		Handle button input
		"""
		print('DemoScene: button state: {}'.format(button_state))
		return 0  # signal that we did not handle the input

	def set_intensity(self, value=None):
		if value is not None:
			self.intensity -= 1
			if not self.intensity:
				self.intensity = 16
		return self.intensity

	def render(self, frame, dropped_frames, fps):
		"""
		Render the scene.
		This method is called by the render loop with the current frame number,
		the number of dropped frames since the previous invocation and the
		requested frames per second (FPS).
		"""
		if (frame % fps) == 0:
			# Only update pixel once every second
			return True

		display = self.display
		intensity = self.intensity

		dot_x, dot_y = self.x_pos, 0
		text_x, text_y = 2, 2
		color = intensity
		display.clear()
		display.put_pixel(dot_x, dot_y, color, color, color >> 1)
		display.render_text(PixelFont, self.text, text_x, text_y, self.intensity)
		display.render()

		self.x_pos += 1
		if self.x_pos == display.columns:
			return False   # signal that our work is done

		return True   # we want to be called again
