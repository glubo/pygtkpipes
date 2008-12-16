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

def GetTileFromConnections(con):
	class direction:
		def __init__(self):
			self.up = False
			self.down = False
			self.left = False
			self.right = False
		def String(self):
			if self.up: string.append('u')
			else: string.append('X')
			if self.down:  string.append('d')
			else: string.append('X')
			if self.left:  string.append('l')
			else: string.append('X')
			if self.right: string.append('r')
			else: string.append('X')
	dir = direction()
	for c in con:
		if c.x == 0:
			if c.y == -1:
				dir.up = True
			elif c.y == 1:
				dir.down = True
		elif c.y == 0:
			if c.x == -1:
				dir.left = True
			elif c.x == 1:
				dir.right = True
	hash = dir.String()
	return HashToTile(hash)

def HashToTile(hash):
	if hash[0] == 'u':
		if hash[1] == 'd':
			if hash[2] == 'l':
				if hash[3] == 'r':
					return Tile(4, 0)
				else:
					return Tile(3, 2)
			elif hash[3] == 'r':
				return Tile(3, 0)
			else:
				return Tile(1, 0)
		elif hash[2] == 'l':
			if hash[3] == 'r':
				return Tile(3, 3)
			else:
				return Tile(2, 2)
		elif hash[3] == 'r':
			return Tile(2, 3)
		else:
			return Tile(0, 2)
	elif hash[1] == 'd':
		if hash[2] == 'l':
			if hash[3] == 'r':
				return Tile(3, 1)
			else:
				return Tile(2, 1)
		elif hash[3] == 'r':
			return Tile(2, 0)
		else:
			return Tile(0, 0)
	elif hash[2] == 'l':
		if hash[3] == 'r':
			return Tile(1, 1)
		else:
			return Tile(0, 1)
	elif hash[3] == 'r':
		return Tile(0, 3)
	else: return Tile(4,0)
		

class Tile:
	def __init__(self, type, rotation, accessible=False, start=False):
		self.type = type
		self.rotation = rotation
		self.accessible = accessible
		self.start = False
		
class PipesGrid:
	def __init__(self, xx=10, yy=10):
		IB = PixBufBank()
		self.widget = gtk.Table(rows=xx, columns=yy, homogeneous = True)
		self.xx = xx
		self.yy = yy
		self.buttons = []
		self.tiles = []
		for y in range(0, yy):
			for x in range(0,xx):
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

	def RegenerateImages(self):
		IB = PixBufBank()
		for y in range(0, self.yy): 
			for x in range(0, self.xx):
				tile = self.GetTile(x,y)
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
	def destroy(self, widget, data=None):
		gtk.main_quit()
	def SetGSize(self, widget, x=None, y=None):
		self.VBox.remove(self.grid.Widget())
		c = Configuration()
		c.GridXX = x
		c.GridYY = y
		self.grid = PipesGrid(c.GridXX, c.GridYY)
		self.grid.Widget().show_all()
		self.VBox.add (self.grid.Widget())
		self.window.resize(1,1)
	def SetTSize(self, widget, size=None):
		if size > 0:
			c = Configuration()
			c.TileSize = size
			IB = PixBufBank()
			IB.LoadImages()
			self.grid.RegenerateImages()
			self.window.resize(1,1)
	def __init__(self):
		c = Configuration()
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.VBox = gtk.VBox()
		self.window.add (self.VBox)

		menu_bar = gtk.MenuBar()
		self.VBox.pack_start(menu_bar, False, False, 2)

		file_menu_i = gtk.MenuItem("_File")
		menu_bar.append (file_menu_i)
		file_menu = gtk.Menu()
		it = gtk.MenuItem('E_xit')
		file_menu.append (it)
		it.connect("activate", self.destroy)
		file_menu_i.set_submenu (file_menu)

		tsize_menu_i = gtk.MenuItem("_Tile Size")
		menu_bar.append (tsize_menu_i)
		tsize_menu = gtk.Menu()
		for i in [5, 10, 15, 20, 30, 40, 50, 60, 70, 80]:
			it = gtk.MenuItem("%d px"%i)
			tsize_menu.append (it)
			it.connect("activate", self.SetTSize, i)
		tsize_menu_i.set_submenu (tsize_menu)

		gsize_menu_i = gtk.MenuItem("_Grid Size")
		menu_bar.append (gsize_menu_i)
		gsize_menu = gtk.Menu()
		for i in [5, 10, 15, 20, 30]:
			it = gtk.MenuItem(repr(i)+'x'+repr(i))
			gsize_menu.append (it)
			it.connect("activate", self.SetGSize, i, i)
		gsize_menu_i.set_submenu (gsize_menu)


		self.grid = PipesGrid(c.GridXX, c.GridYY)
		self.VBox.add (self.grid.Widget())
		self.window.show_all()
	def main(self):
		gtk.main()
if __name__ == "__main__":
	hello = Hello()
	hello.main()
