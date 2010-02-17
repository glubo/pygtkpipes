#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration
from pixbufbank import PixBufBank
from tilewidget import TileWidget
from grid import *

class PipesGrid:
	def __init__(self, xx=10, yy=10):
		IB = PixBufBank()
		self.widget = gtk.Table(rows=xx, columns=yy, homogeneous = True)
		self.xx = xx
		self.yy = yy
		self.sx = xx/2
		self.sy = yy/2
		self.tiles = GenerateTileGrid(xx, yy, self.sx, self.sy)
		self.Shake()
		self.RegenerateWGrid()
	
	def UpdateAccess(self):
		looseends = []
		def XY2I(x,y):
			return x+y*self.xx
		def I2VEC(i):
			return Vec2(i%self.xx, i/self.xx)
		def IsConnectedAndValidMove (i_o, dir):
			t_o = self.tiles[i_o]
			pos_o = I2VEC (i_o)
			pos_d = Vec2 (pos_o.x + dir.x, pos_o.y + dir.y)
			if not (0 <= pos_d.x < self.xx) or not (0 <= pos_d.y < self.yy):
				return False
			i_d = XY2I(pos_d.x, pos_d.y)
			t_d = self.tiles[i_d]
			if t_d.accessible:
				return False
			con_o = GetConnections(t_o.type, t_o.rotation)
			con_d = GetConnections(t_d.type, t_d.rotation)
			o_d = False
			d_o = False
			for con in con_o:
				if con.x == dir.x and con.y == dir.y:
					o_d = True
			for con in con_d:
				if con.x == 0-dir.x and con.y == 0-dir.y:
					d_o = True
			return o_d and d_o
		for i in range(0, self.xx*self.yy):
			self.tiles[i].accessible = False
		looseends.append (XY2I (self.sx, self.sy))
		connected = 0
		while looseends.__len__() > 0:
			i_o = looseends[0]
			looseends.remove(i_o)
			for d in [Vec2(-1,0), Vec2(0,1), Vec2(1,0), Vec2(0,-1)]:
				if IsConnectedAndValidMove(i_o, d):
					pos_o = I2VEC(i_o)
					pos_d = Vec2(pos_o.x + d.x, pos_o.y + d.y)
					i_d = XY2I(pos_d.x, pos_d.y)
					t_d = self.tiles[i_d]
					t_d.accessible = True
					looseends.append(i_d)
					connected += 1
		if connected == self.xx*self.yy:
			self.Solved = True
			self.OnSolved()
		else:
			self.Solved = False
			

	def OnSolved(self):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Congratulations!\nYou have completed this puzzle.")
		dialog.run()
		dialog.destroy()
	def Shake(self):
		for tile in self.tiles:
			tile.rotation = random.randint(0, GetRotations(tile.type)-1)
	def RegenerateWGrid(self):
		self.Focus_x = 0
		self.Focus_y = 0
		self.buttons = []
		self.widget = gtk.Table(rows=self.xx, columns=self.yy, homogeneous = True)
		self.widget.set_flags(gtk.CAN_FOCUS)
		self.widget.grab_focus()
		self.widget.add_events(gtk.gdk.KEY_PRESS_MASK)
		self.widget.connect ("key-press-event", self.KeyPress)
		for y in range(0, self.yy):
			for x in range(0, self.xx):
				tile = self.GetTile(x, y)
				type = tile.type;
				rotation = tile.rotation
				accessible = tile.accessible
				self.buttons.append(TileWidget(tile))
				but = self.GetButton(x, y)
				self.widget.attach(but, x, x+1, y, y+1, xoptions=gtk.SHRINK, yoptions=gtk.SHRINK)
				but.connect("button-press-event", self.ButClick, x, y)
		self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
	def KeyPress(self, widget, event):
		name = gtk.gdk.keyval_name (event.keyval)
		redraw = False
		if name == 'Up':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_y > 0: self.Focus_y -= 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'Down':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_y < self.yy-1: self.Focus_y += 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'Left':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_x > 0: self.Focus_x -= 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'Right':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_x < self.xx-1: self.Focus_x += 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'space':
			self.ButClicked(self, self.Focus_x, self.Focus_y)
		if redraw:
			self.widget.queue_draw()
		return True
	def ButClick(self, widget,event, x, y):
		if (event.button == 1 or event.button == 3) and event.type == gtk.gdk.BUTTON_PRESS:
			self.ButClicked(widget, x, y, event.button)
		return True
	def ButClicked(self, widget, x, y, button=1):
		tile = self.GetTile(x,y)
		rot = 0
		if button == 1:
			rot = 1
		elif button == 3:
			rot = -1
		tile.rotation = (tile.rotation + rot) % GetRotations(tile.type)
		self.UpdateAccess()
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
	def SetTDesign(self, widget, design=None):
		c = Configuration()
		IB = PixBufBank()
		IB.SetDesign (design)
		IB.LoadImages()
		self.VBox.remove(self.grid.Widget())
		self.grid.RegenerateImages()
		self.grid.Widget().show_all()
		self.VBox.add (self.grid.Widget())
		self.window.resize(1,1)
		
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
		self.window.set_title('PyGtkPipes')
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

		gsize_menu_i = gtk.MenuItem("_New Puzzle")
		menu_bar.append (gsize_menu_i)
		gsize_menu = gtk.Menu()
		for i in [5, 10, 15, 20, 30]:
			it = gtk.MenuItem(repr(i)+'x'+repr(i))
			gsize_menu.append (it)
			it.connect("activate", self.SetGSize, i, i)
		gsize_menu_i.set_submenu (gsize_menu)

		tdesign_menu_i = gtk.MenuItem("_Design")
		menu_bar.append (tdesign_menu_i)
		tdesign_menu = gtk.Menu()
		for i in [1, 2]:
			it = gtk.MenuItem("%d"%i)
			tdesign_menu.append (it)
			it.connect("activate", self.SetTDesign, i)
		tdesign_menu_i.set_submenu (tdesign_menu)


		self.grid = PipesGrid(c.GridXX, c.GridYY)
		self.VBox.add (self.grid.Widget())

		#TODO: test on windows
		iconpixbuf = gtk.gdk.pixbuf_new_from_file('design1/cross.svg')
		self.window.set_icon(iconpixbuf)

		self.window.show_all()
		self.SetTSize(None, c.TileSize) #ugly hack to show widgets at start
	def main(self):
		gtk.main()
if __name__ == "__main__":
	hello = Hello()
	hello.main()
