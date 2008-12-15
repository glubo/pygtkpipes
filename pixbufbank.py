import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration

class PixBufBank:
	def GetPixBuf(self, type, rotation, accessible):
		return self.I[rotation]
	def LoadImages(self):
		c = Configuration()
		self.I = []
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/I.svg', c.TileSize, c.TileSize))
		self.I.append(self.I[0].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))
	#below is singleton implementation
	class __impl:
		pass

	__instance = None

	def __init__(self):
		# Check if we already have an instance
		if PixBufBank.__instance is None:
			# Create and remember instance
			PixBufBank.__instance = PixBufBank.__impl()
			self.LoadImages()

		# Store instance reference as the only member in the handle
		self.__dict__['_PixBufBank__instance'] = PixBufBank.__instance

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		return setattr(self.__instance, attr, value)
