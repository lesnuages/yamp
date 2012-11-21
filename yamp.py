#! /usr/bin/python2

import sys, os
import pygtk, gtk, gobject
from player import MusicPlayer

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
        self.menuOpen.connect("activate", self.open_file_dialog)
        self.menuExit = gtk.MenuItem("Exit")
        self.menuExit.connect("activate", gtk.main_quit)

        self.filemenu.append(self.menuOpen)
        self.filemenu.append(self.menuExit)

        self.mb.append(self.filem)

        vbox = gtk.VBox(False, 2)
        window.add(vbox)
        vbox.pack_start(self.mb, False, False, 0)

        self.imgStop = gtk.Image()
        self.imgPlay = gtk.Image()
        self.imgNext = gtk.Image()
        self.imgPrev = gtk.Image()
        self.imgPause = gtk.Image()

        self.imgStop.set_from_stock(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_BUTTON)
        self.imgPause.set_from_stock(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_BUTTON)
        self.imgPlay.set_from_stock(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON)
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
        self.buttonPlay.add(self.imgPlay)
        self.buttonPrev.add(self.imgPrev)
        self.buttonNext.add(self.imgNext)

        self.buttonPlay.connect("clicked", self.play_action)
        self.buttonNext.connect("clicked", self.next_action)
        self.buttonPrev.connect("clicked", self.prev_action)
        self.buttonStop.connect("clicked", self.stop_action)

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
        hbox.pack_start(vboxInfos, False, False, 8)

        vbox.pack_start(hbox, False, False, 5)
        window.show_all()

        self.player = MusicPlayer()
        self.player.add_observer(self)

    def update(self,message=None):
        if message == "reset":
            self.buttonPlay.set_image(self.imgPlay)
            self.isPlaying = False
        elif message == "pause":
            self.buttonPlay.set_image(self.imgPlay)
            self.isPlaying = False
        elif message == "play":
            self.buttonPlay.set_image(self.imgPause)
            self.isPlaying = True
        else:
            print("Error : unknow message {}".format(message))

    def play_action(self, w):
        if w == self.buttonPlay:
            if self.isPlaying:
                self.player.pause()
            else:
                if not self.isPlaying and os.path.isfile(self.filePath):
                    self.player.open_file(self.filePath)
                self.player.play()

    def next_action(self, w):
        if w == self.buttonNext:
            self.player.play_next()

    def prev_action(self, w):
        if w == self.buttonPrev:
            self.player.play_prev()

    def stop_action(self, w):
        if w == self.buttonStop:
            self.player.stop()

    def open_file_dialog(self, w):
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
