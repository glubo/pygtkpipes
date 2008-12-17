#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import random

from configuration  import Configuration
from pixbufbank import PixBufBank
from tilewidget import TileWidget

class Vec2:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	def __str__(self):
		return "["+str(self.x)+":"+str(self.y)+"]"
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

def GenerateTileGrid(xx,yy,sx,sy):
	grid = []
	tgrid = []
	looseends = []

	for i in range(0,xx*yy):
		grid.append([False,[]])
	
	def XY2I(x,y):
		return x+y*xx
	def I2VEC(i):
		return Vec2(i%xx, i/xx)
	def Tile(x,y):
		return grid[XY2I(x,y)]
	def TTile(x,y):
		return tgrid[XY2I(x,y)]
	def IsAllReachable():
		for i in range(0,xx*yy):
			if grid[i][0] == False:
				return False
		return True
	def IsUnreached(x,y):
		if (not (0 <= x < xx)) or (not (0 <= y < yy)):
			return False
		return  not Tile(x,y)[0]
	def PickOneLooseEndID():
		return random.choice(looseends)
	def PickOneFreeDirectionFromID(i):
		pos = I2VEC(i)
		dirs = [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]
		random.shuffle(dirs)
		for d in dirs:
			if IsUnreached (pos.x + d.x, pos.y + d.y):
				return d
		else: print "No Free Direction :-X"
	def GridToTGrid():
		del tgrid[:]
		for i in range (0, xx*yy):
			tgrid.append (GetTileFromConnections (grid[i][1]))
		tgrid[XY2I (sx, sy)].accessible = True
		tgrid[XY2I (sx, sy)].start = True
	def PrintGrid():
		GridToTGrid()
		for x in range(0,xx):
			line = ''
			for y in range(0,yy):
				line += str(TTile(y,x))
			print line

	def CleanLooseEnds():
		lc = looseends[:]
		for id in lc:
			DeleteFromLoosendsIfAppropriate(id)
	def DeleteFromLoosendsIfAppropriate(i):
		if not looseends.__contains__(i):
			return
		remove = True
		pos = I2VEC (i)
		for d in [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]:
			if IsUnreached (pos.x + d.x, pos.y + d.y):
				remove = False
		if remove:
			looseends.remove(i)

	Tile(sx,sy)[0] = True
	looseends.append(XY2I(sx,sy))
	while not IsAllReachable ():
		i = PickOneLooseEndID ()
		direction = PickOneFreeDirectionFromID(i)

		t_pos = I2VEC (i)
		tile = grid[i]

		d_pos = Vec2 (t_pos.x + direction.x, t_pos.y + direction.y)
		d_i = XY2I (d_pos.x, d_pos.y) 
		dtile = grid[d_i]

		dtile[0] = True
		tile[1].append (direction)
		dtile[1].append (Vec2 (0 - direction.x, 0 - direction.y))
		looseends.append(d_i)
		CleanLooseEnds()

	#here we have already grid full, now only convert to hgrid:
	GridToTGrid()
	PrintGrid()
	return tgrid

	
def GetTileFromConnections(con):
	class direction:
		def __init__(self):
			self.up = False
			self.down = False
			self.left = False
			self.right = False
		def String(self):
			string = ''
			if self.up: string+='u'
			else: string+='X'
			if self.down:  string+='d'
			else: string+='X'
			if self.left:  string+='l'
			else: string+='X'
			if self.right: string+='r'
			else: string+='X'
			return string
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
	def __str__(self):
		if self.type == 0:
			if self.rotation == 0: return 'V'
			if self.rotation == 1: return '<'
			if self.rotation == 2: return '^'
			if self.rotation == 3: return '>'
		if self.type == 1:
			if self.rotation == 0: return '|'
			if self.rotation == 1: return '-'
		if self.type == 2:
			if self.rotation == 0: return 'L'
			if self.rotation == 1: return 'L'
			if self.rotation == 2: return 'L'
			if self.rotation == 3: return 'L'
		if self.type == 3:
			if self.rotation == 0: return 'T'
			if self.rotation == 1: return 'T'
			if self.rotation == 2: return 'T'
			if self.rotation == 3: return 'T'
		if self.type == 4:
			return '+'
		return 'tile'
		
class PipesGrid:
	def __init__(self, xx=10, yy=10):
		IB = PixBufBank()
		self.widget = gtk.Table(rows=xx, columns=yy, homogeneous = True)
		self.xx = xx
		self.yy = yy
		self.tiles = GenerateTileGrid(xx, yy, xx/2, yy/2)
		self.Shake()
		self.RegenerateWGrid()
	
	def Shake(self):
		for tile in self.tiles:
			tile.rotation = random.randint(0, GetRotations(tile.type)-1)
	def RegenerateWGrid(self):
		self.buttons = []
		self.widget = gtk.Table(rows=self.xx, columns=self.yy, homogeneous = True)
		for y in range(0, self.yy):
			for x in range(0, self.xx):
				tile = self.GetTile(x, y)
				type = tile.type;
				rotation = tile.rotation
				accessible = tile.accessible
				self.buttons.append(TileWidget(tile))
				but = self.GetButton(x, y)
				self.widget.attach(but, x, x+1, y, y+1)
				but.connect("button-press-event", self.ButClicked, x, y)
	def ButClicked(self, widget,event, x, y):
		tile = self.GetTile(x,y)
		tile.rotation = (tile.rotation + 1) % GetRotations(tile.type)
		self.widget.queue_draw()

	def RegenerateImages(self):
		self.RegenerateWGrid()
		
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
			self.VBox.remove(self.grid.Widget())
			self.grid.RegenerateImages()
			self.grid.Widget().show_all()
			self.VBox.add (self.grid.Widget())
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
		self.SetTSize(None, c.TileSize) #ugly hack to show widgets at start
	def main(self):
		gtk.main()
if __name__ == "__main__":
	hello = Hello()
	hello.main()
