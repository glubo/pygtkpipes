#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration
from pixbufbank import PixBufBank

class Vec2:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
# Tile types:
# 0: end
# 1: I
# 2: L
# 3: T
# 4: +

def GetRotations(type):
	if type == 0:
		return 4
	elif type == 1:
		return 2
	elif type == 2:
		return 4
	elif type == 3:
		return 4
	elif type == 4:
		return 1
	else: return 1

def GetConnections(type, rotation):
	if type == 0:
		if rotation == 0:
			return [Vec2(0,1)]
		elif rotation == 1:
			return [Vec2(-1,0)]
		elif rotation == 2:
			return [Vec2(0,-1)]
		elif rotation == 3:
			return [Vec2(1,0)]
	elif type == 1:
		if (rotation % 2) == 0:
			return [Vec2(0,-1), Vec2(0, 1)]
		else:
			return [Vec2(-1,0), Vec2(1, 0)]
	if type == 2:
		if rotation == 0:
			return [Vec2(0,1), Vec2(1,0)]
		elif rotation == 1:
			return [Vec2(0,1), Vec2(-1,0)]
		elif rotation == 2:
			return [Vec2(0,-1), Vec2(-1,0)]
		elif rotation == 3:
			return [Vec2(0,-1), Vec2(1,0)]
	if type == 3:
		if rotation == 0:
			return [Vec2(0,1), Vec2(0,-1), Vec2(1,0)]
		elif rotation == 1:
			return [Vec2(0,1), Vec2(1,0), Vec2(0,1)]
		elif rotation == 2:
			return [Vec2(0,1), Vec2(0,-1), Vec2(-1,0)]
		elif rotation == 3:
			return [Vec2(0,-1), Vec2(1,0), Vec2(-1,0)]
	if type == 4:
		return [Vec2(0,1), Vec2(0,-1), Vec2(1,0), Vec2(-1,0)]
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
				type = (x+y)%5;
				rotation = 0*x%GetRotations(type)
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
