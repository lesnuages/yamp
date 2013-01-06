#! /usr/bin/env python2

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	print("Error importing gtk / gtk.glade")
	sys.exit(1)

class Yamp:
	def __init__(self):
		self.glade = gtk.Builder()
		self.glade_file = "yamp.glade"
		self.glade.add_from_file(self.glade_file)

		self.window = self.glade.get_object("winMain")
		if self.window:
			self.window.connect("destroy", gtk.main_quit)
		self.window.show_all()

if __name__ == "__main__":
	yamp = Yamp()
	gtk.main()