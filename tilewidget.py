#!/usr/bin/env python


try:
	import gtk
  	import gobject
  	from gtk import gdk
except:
	raise SystemExit
	

import pygtk
if gtk.pygtk_version < (2, 0):
  	print "PyGtk 2.0 or later required for this widget"
  	raise SystemExit

from pixbufbank import PixBufBank
from configuration  import Configuration
  

class TileWidget(gtk.Widget):
	
	def __init__(self, tile):
		
		#Initialize the Widget
		gtk.Widget.__init__(self)
		
		self.tile = tile
		
	def do_realize(self):
		
		self.set_flags(self.flags() | gtk.REALIZED)
		
			
		self.window = gtk.gdk.Window(
			self.get_parent_window(),
			width=self.allocation.width,
			height=self.allocation.height,
			window_type=gdk.WINDOW_CHILD,
			wclass=gdk.INPUT_OUTPUT,
			event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK
				| gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK
				| gtk.gdk.POINTER_MOTION_MASK
				| gtk.gdk.POINTER_MOTION_HINT_MASK)
				
		# Associate the gdk.Window with ourselves
		self.window.set_user_data(self)
		
		# Attach the style to the gdk.Window
		self.style.attach(self.window)
		
		# The default color of the background should be what
		# the style (theme engine) tells us.
		self.style.set_background(self.window, gtk.STATE_NORMAL)
		self.window.move_resize(*self.allocation)
		
			
		# self.style is a gtk.Style object, self.style.fg_gc is
		# an array or graphic contexts used for drawing the forground
		# colours	
		self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
		
		
	def do_unrealize(self):
		# The do_unrealized method is responsible for freeing the GDK resources
		# De-associate the window we created in do_realize with ourselves
		self.window.destroy()
		
	def do_size_request(self, requisition):
		c = Configuration()
		requisition.height = c.TileSize
		requisition.width = c.TileSize
	
	
	def do_size_allocate(self, allocation):
		if self.flags() & gtk.REALIZED:
			self.window.move_resize(*allocation)
		
	def do_expose_event(self, event):
		"""This is where the widget must draw itself."""
		PB = PixBufBank()
		t = self.tile
		
		self.window.draw_pixbuf(self.gc, PB.GetPixBuf(t.type, t.rotation, t.accessible), 0, 0, 0, 0,-1, -1)	
		return True
			
			
	def queue_drawing(self):
		self.window.invalidate_rect(self.allocation,True)
			
			
gobject.type_register(TileWidget)

if __name__ == "__main__":
	# register the class as a Gtk widget
	
	win = gtk.Window()
	win.connect('delete-event', gtk.main_quit)
	class Tile:
		pass
	t = Tile()
	t.type =3
	t.rotation = 2
	t.accessible = False
	TileW = TileWidget(t)
	win.add(TileW)
	
	win.show_all()    
	win.resize(1,1)
	gtk.main()
	
