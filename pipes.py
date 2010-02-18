#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from configuration  import Configuration
from pixbufbank import PixBufBank
from tilewidget import TileWidget
import grid 
import random
import PipesGrid

				
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
		self.grid = PipesGrid.PipesGrid(c.GridXX, c.GridYY)
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


		self.grid = PipesGrid.PipesGrid(c.GridXX, c.GridYY)
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
