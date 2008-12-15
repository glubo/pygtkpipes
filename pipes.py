#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration
from pixbufbank import PixBufBank

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

class Vec2:
	def __init__(self, x=0., y=0.):
		self.x = x
		self.y = y
# Tile types:
# 0: end
# 1: I
# 2: L
# 3: T
# 4: +

def GetRotations(type):
	if type == 1:
		return 2
	else: return 1
def GetConnections(type, rotation):
	if type == 1:
		if (rotation % 2) == 0:
			return [Vec2(-1.,0.), Vec2(1., 0.)]
		else:
			return [Vec2(0.,-1.), Vec2(0., 1.)]
	else: return []

class Tile:
	def __init__(self, type, rotation, accessible=False):
		self.type = type
		self.rotation = rotation
		self.accessible = accessible
		
class PipesGrid:
	def __init__(self, xx=10, yy=10):
		self.widget = gtk.Table(rows=xx, columns=yy, homogeneous = True)
		self.xx = xx
		self.yy = yy
		self.buttons = []
		self.tiles = []
		for y in range(0, yy):
			for x in range(0,xx):
				IB = PixBufBank()
				type = 1
				rotation = x%2
				accessible = False
				self.buttons.append(gtk.Button())
				but = self.GetButton(x, y)
				but.set_border_width(0)
				but.add (gtk.image_new_from_pixbuf(IB.GetPixBuf(type, rotation, accessible)))
				self.widget.attach(but, x, x+1, y, y+1)
				but.connect("clicked", self.ButClicked, x, y)
				self.tiles.append(Tile(type, rotation, accessible))
	def ButClicked(self, widget, x, y):
		IB = PixBufBank()
		tile = self.GetTile(x,y)
		tile.rotation = (tile.rotation + 1) % GetRotations(tile.type)
		but = self.GetButton(x,y)
		but.remove (but.get_child())
		but.add (gtk.image_new_from_pixbuf(IB.GetPixBuf(tile.type, tile.rotation, tile.accessible)))
		but.get_child().show()

	def GetButton(self, x, y):
		return self.buttons[x+(y)*self.xx]
	def GetTile(self, x, y):
		return self.tiles[x+(y)*self.xx]
	def Widget(self):
		return self.widget
				
class Hello:
	def hello(self, widget, data=None):
		print "Hello World!!!"
	def destroy(self, widget, data=None):
		gtk.main_quit()
	def __init__(self):
		c = Configuration()
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.grid = PipesGrid(c.GridXX, c.GridYY)
		self.window.add (self.grid.Widget())
		self.window.show_all()
	def main(self):
		gtk.main()
if __name__ == "__main__":
	hello = Hello()
	hello.main()
