#! /usr/bin/env python

import pygtk, gtk, gobject
from player import MusicPlayer
from playlist import Song

class GTK_Main:

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Yamp!")
        window.set_default_size(450, 300)
        window.connect("destroy", gtk.main_quit, "WM destroy")
        window.set_position(gtk.WIN_POS_CENTER)
        
        self.player = MusicPlayer()
        self.player.add_observer(self)

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

        self.lblArtist = gtk.Label()
        self.lblAlbum = gtk.Label()
        self.lblSongTitle = gtk.Label()

        self.lblArtist.set_use_markup(True)
        self.lblAlbum.set_use_markup(True)
        self.lblSongTitle.set_use_markup(True)

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
        pixbuf = gtk.gdk.pixbuf_new_from_file("music_cd.png")
        scaled_buf = pixbuf.scale_simple(84,84,gtk.gdk.INTERP_BILINEAR)
        self.imgCover.set_from_pixbuf(scaled_buf)

        self.sw = gtk.ScrolledWindow()
        self.sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        store = self.create_model()

        self.treeView = gtk.TreeView(store)
        self.treeView.connect("row-activated", self.on_activated)
        self.treeView.set_rules_hint(True)
        self.sw.add(self.treeView)
        self.create_columns(self.treeView)

        hboxButtons = gtk.HBox(False, 5)
        hboxButtons.pack_start(self.buttonPrev, False, False, 0)
        hboxButtons.pack_start(self.buttonPlay, False, False, 0)
        hboxButtons.pack_start(self.buttonStop, False, False, 0)
        hboxButtons.pack_start(self.buttonNext, False, False, 0)


        vboxInfos = gtk.VBox(False, 0)
        self.lblSongTitle.set_alignment(0,0.5)
        self.lblArtist.set_alignment(0,0.5)
        self.lblAlbum.set_alignment(0,0.5)
        vboxInfos.pack_start(hboxButtons, True, True, 0)
        vboxInfos.pack_start(self.lblSongTitle, True, True, 0)
        vboxInfos.pack_start(self.lblArtist, True, True, 0)
        vboxInfos.pack_start(self.lblAlbum, True, True, 0)
        
        hbox = gtk.HBox(False,10)
        hbox.pack_start(self.imgCover, False, False, 0)
        hbox.pack_start(vboxInfos, False, False, 0)

        vbox.pack_start(hbox, False, False, 5)
        vbox.pack_start(self.sw, True, True, 0)
        window.show_all()

    def update(self,message=None, song=None):
        if message == "reset":
            self.buttonPlay.set_image(self.imgPlay)
        elif message == "pause":
            self.buttonPlay.set_image(self.imgPlay)
        elif message == "play":
            if song is not None:
                self.lblArtist.set_markup("<b>"+song.get_artist()+"</b>")
                self.lblAlbum.set_markup("<b>"+song.get_album()+"</b>")
                self.lblSongTitle.set_markup("<b>#{} - {}</b>".format(song.get_track(),song.get_title()))
            self.buttonPlay.set_image(self.imgPause)
        elif message == "update_playlist":
            self.update_model()
        else:
            print("Error : unknow message {}".format(message))


    def update_model(self):
        for song in self.player.get_playlist():
            self.treeView.get_model().append([song.get_track(),song.get_title(),song.get_artist(),song.get_album(),song.get_path()])

    def create_model(self):
        store = gtk.ListStore(str,str,str,str,str) 
        return store

    def on_activated(self, widget, row, col):
        model = widget.get_model()
        song = Song(model[row][1],model[row][2],model[row][3],model[row][0],model[row][4])
        if self.player.is_playing():
            self.player.stop()
        self.player.play(song)

    def create_columns(self, treeView):
            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn("Track #", rendererText, text=0)
            column.set_sort_column_id(0)    
            treeView.append_column(column)
            
            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn("Title", rendererText, text=1)
            column.set_sort_column_id(1)
            treeView.append_column(column)

            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn("Artist", rendererText, text=2)
            column.set_sort_column_id(2)
            treeView.append_column(column)

            rendererText = gtk.CellRendererText()
            column = gtk.TreeViewColumn("Album", rendererText, text=3)
            column.set_sort_column_id(3)
            treeView.append_column(column)

    def play_action(self, w):
        if w == self.buttonPlay:
            if self.player.is_playing():
                self.player.pause()
            else:
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
        chooser = gtk.FileChooserDialog("Open",action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_select_multiple(True)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filenames = chooser.get_filenames()
            self.player.stop()
            self.update("reset")
            self.player.set_playlist(filenames)

        chooser.destroy()

GTK_Main()
gtk.gdk.threads_init()
gtk.main()
