#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration
from pixbufbank import PixBufBank
from tilewidget import TileWidget
import grid 
import random

class PipesGrid:
	def __init__(self, xx=10, yy=10):
		IB = PixBufBank()
		self.widget = gtk.Table(rows=xx, columns=yy, homogeneous = True)
		self.grid = grid.Grid (xx, yy)
		self.grid.Shake()
		self.RegenerateWGrid()
	
	def UpdateAccess(self):
		self.grid.UpdateAccess ()
		if self.grid.IsSolved():
			self.OnSolved()

	def OnSolved(self):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "Congratulations!\nYou have completed this puzzle.")
		dialog.run()
		dialog.destroy()
	def RegenerateWGrid(self):
		self.Focus_x = 0
		self.Focus_y = 0
		self.buttons = []
		self.widget = gtk.Table(rows=self.grid.xx, columns=self.grid.yy, homogeneous = True)
		self.widget.set_flags(gtk.CAN_FOCUS)
		self.widget.grab_focus()
		self.widget.add_events(gtk.gdk.KEY_PRESS_MASK)
		self.widget.connect ("key-press-event", self.KeyPress)
		for y in range(0, self.grid.yy):
			for x in range(0, self.grid.xx):
				tile = self.grid.GetTile(x, y)
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
			if self.Focus_y < self.grid.yy-1: self.Focus_y += 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'Left':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_x > 0: self.Focus_x -= 1
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = True
			redraw = True
		elif name == 'Right':
			self.GetButton (self.Focus_x, self.Focus_y).MyFocus = False
			if self.Focus_x < self.grid.xx-1: self.Focus_x += 1
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
		rot = 0
		if button == 1:
			rot = 1
		elif button == 3:
			rot = -1
		self.grid.Rotate (x, y, rot)
		self.UpdateAccess()
		self.widget.queue_draw()

	def RegenerateImages(self):
		self.RegenerateWGrid()
		
	def GetButton(self, x, y):
		return self.buttons[x+(y)*self.grid.xx]
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
