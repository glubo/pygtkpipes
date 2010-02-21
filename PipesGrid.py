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
		self.UpdateAccess ()
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
