import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration

class PixBufBank:
	def GetPixBuf(self, type, rotation, accessible):
		offset = 15 if accessible else 0
		if type == 0:
			return self.I[rotation+offset]
		elif type == 1:
			return self.I[rotation+4+offset]
		elif type == 2:
			return self.I[rotation+6+offset]
		elif type == 3:
			return self.I[rotation+10+offset]
		elif type == 4:
			return self.I[14+offset]
	def LoadImages(self):
		c = Configuration()
		self.I = []
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/end.svg', c.TileSize, c.TileSize))#0
		self.I.append(self.I[0].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#1
		self.I.append(self.I[1].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#2
		self.I.append(self.I[2].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#3
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/I.svg', c.TileSize, c.TileSize))#4
		self.I.append(self.I[4].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#5

		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/L.svg', c.TileSize, c.TileSize))#6
		self.I.append(self.I[6].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#7
		self.I.append(self.I[7].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#8
		self.I.append(self.I[8].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#9
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/T.svg', c.TileSize, c.TileSize))#10
		self.I.append(self.I[10].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#11
		self.I.append(self.I[11].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#12
		self.I.append(self.I[12].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#13
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/cross.svg', c.TileSize, c.TileSize))#14

		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/endc.svg', c.TileSize, c.TileSize))#15
		self.I.append(self.I[15].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#16
		self.I.append(self.I[16].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#17
		self.I.append(self.I[17].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#18
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/Ic.svg', c.TileSize, c.TileSize))#19
		self.I.append(self.I[19].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#20

		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/Lc.svg', c.TileSize, c.TileSize))#21
		self.I.append(self.I[21].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#22
		self.I.append(self.I[22].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#23
		self.I.append(self.I[23].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#24
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/Tc.svg', c.TileSize, c.TileSize))#25
		self.I.append(self.I[25].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#26
		self.I.append(self.I[26].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#27
		self.I.append(self.I[27].rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE))#28
		self.I.append(gtk.gdk.pixbuf_new_from_file_at_size('design1/crossc.svg', c.TileSize, c.TileSize))#29

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
