#! /usr/bin/python2

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require('0.10')
import gst

class GTK_Main:

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Yamp!")
        window.set_default_size(300, -1)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        window.set_position(gtk.WIN_POS_CENTER)

        self.filePath = ""
        self.isPlaying = False

        self.mb = gtk.MenuBar()
        self.filemenu = gtk.Menu()
        
        self.filem = gtk.MenuItem("File")
        self.filem.set_submenu(self.filemenu)
        
        self.menuOpen = gtk.MenuItem("Open")
        self.menuOpen.connect("activate", self.openFileDialog)
        self.menuExit = gtk.MenuItem("Exit")
        self.menuExit.connect("activate", gtk.main_quit)

        self.filemenu.append(self.menuOpen)
        self.filemenu.append(self.menuExit)

        self.mb.append(self.filem)

        vbox = gtk.VBox(False, 2)
        window.add(vbox)
        vbox.pack_start(self.mb, False, False, 0)
        self.imgStop = gtk.Image()
        self.imgStart = gtk.Image()
        self.imgNext = gtk.Image()
        self.imgPrev = gtk.Image()
        self.imgPause = gtk.Image()
        self.imgStop.set_from_stock(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_BUTTON)
        self.imgPause.set_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_BUTTON)
        self.imgStart.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
        self.imgPrev.set_from_stock(gtk.STOCK_MEDIA_PREVIOUS, gtk.ICON_SIZE_BUTTON)
        self.imgNext.set_from_stock(gtk.STOCK_MEDIA_NEXT, gtk.ICON_SIZE_BUTTON)

        self.lblArtist = gtk.Label("Artist")
        self.lblAlbum = gtk.Label("Album")
        self.lblSongTitle = gtk.Label("Song Title")

        self.buttonPlay = gtk.Button()
        self.buttonNext = gtk.Button()
        self.buttonPrev = gtk.Button()
        self.buttonStop = gtk.Button()

        self.buttonStop.set_relief(gtk.RELIEF_NONE)
        self.buttonPlay.set_relief(gtk.RELIEF_NONE)
        self.buttonPrev.set_relief(gtk.RELIEF_NONE)
        self.buttonNext.set_relief(gtk.RELIEF_NONE)

        self.buttonStop.add(self.imgStop)
        self.buttonPlay.add(self.imgStart)
        self.buttonPrev.add(self.imgPrev)
        self.buttonNext.add(self.imgNext)

        self.buttonPlay.connect("clicked", self.playAction)
        self.buttonNext.connect("clicked", self.nextAction)
        self.buttonPrev.connect("clicked", self.prevAction)
        self.buttonStop.connect("clicked", self.stopAction)

        self.imgCover = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("cd_case.png")
        scaled_buf = pixbuf.scale_simple(84,84,gtk.gdk.INTERP_BILINEAR)
        self.imgCover.set_from_pixbuf(scaled_buf)

        hboxButtons = gtk.HBox(False, 5)
        hboxButtons.pack_start(self.buttonPrev, False, False, 0)
        hboxButtons.pack_start(self.buttonPlay, False, False, 0)
        hboxButtons.pack_start(self.buttonStop, False, False, 0)
        hboxButtons.pack_start(self.buttonNext, False, False, 0)

        vboxInfos = gtk.VBox(False, 2)
        vboxInfos.pack_start(hboxButtons, True, False, 0)
        vboxInfos.pack_start(self.lblArtist, True, False, 0)
        vboxInfos.pack_start(self.lblAlbum, True, False, 0)
        vboxInfos.pack_start(self.lblSongTitle, True, False, 0)
        
        hbox = gtk.HBox(False,10)
        hbox.pack_start(self.imgCover, False, False, 0)
        hbox.pack_start(vboxInfos, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)
        window.show_all()

        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink",fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def playAction(self, w):
        if w == self.buttonPlay:
            if self.isPlaying:
                self.player.set_state(gst.STATE_PAUSED)
                w.set_image(self.imgStart)
                self.isPlaying = False
            else:
                """ Handle the first click on the Play Button """
                if not self.isPlaying: 
                    if os.path.isfile(self.filePath):
                        self.player.set_property("uri", "file://" + self.filePath)
                    w.set_image(self.imgPause)
                else:
                    w.set_image(self.imgStart)
                self.player.set_state(gst.STATE_PLAYING)
                self.isPlaying = True

    def nextAction(self, w):
        print ("NEXT !")

    def prevAction(self, w):
        print("PREVIOUS !")

    def stopAction(self, w):
        if w == self.buttonStop:
            self.player.set_state(gst.STATE_NULL)
            self.buttonPlay.set_image(self.imgStart)
            self.isPlaying = False

    def on_message(self, bus, message):
        t = message.type;
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.buttonPlay.set_image(self.imgStart)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print ("Error {} {}".format(err, debug))
            self.buttonPlay.set_image(self.imgStart)
    
    def openFileDialog(self, w):
        chooser = gtk.FileChooserDialog("Open",
                                        action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_select_multiple(True)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filenames = chooser.get_filenames()
            if len(filenames) == 1 :
                self.filePath = chooser.get_filename()
            elif len(filenames) > 1:
                playlist = filenames

        chooser.destroy()

GTK_Main()
gtk.gdk.threads_init()
gtk.main()
