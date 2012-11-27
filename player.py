import sys, os
import pygst
pygst.require('0.10')
import gst
from hsaudiotag import auto
from playlist import Playlist

class MusicPlayer:

    def __init__(self):
        self.observers = list()
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.playing = False
        self.playlist = Playlist("New playlist")
        self.currentFile = None


    def is_playing(self):
        return self.playing

    def set_current_file(self,cfile):
        self.currentFile = cfile

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message, infos=None):
        for obs in self.observers:
            obs.update(message, infos)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.notify_observers("reset")
            self.play_next()
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print ("Error {} {}".format(err, debug))
            self.notify_observers("reset")

    def set_playlist(self,pl):
        if len(pl) > 0:
            self.playlist = Playlist("New Playlist", pl)
            self.currentFile = self.playlist.get_current()

    def open_file(self):
        self.player.set_property("uri", "file://" + self.currentFile)

    def play(self):
        if self.currentFile is not None:
            mfile = auto.File(self.currentFile)
            fileInfos = dict()
            fileInfos.update({"artist":mfile.artist, "album":mfile.album, "title":mfile.title, "track_number":mfile.track})
            if not self.is_playing():
                self.open_file()
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
            self.notify_observers("play", fileInfos)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.playing = False
        self.notify_observers("pause")

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.notify_observers("reset")
        self.playing = False

    def play_next(self):
        self.stop()
        self.currentFile = self.playlist.get_next_track()
        self.play()

    def play_prev(self):
        self.stop()
        self.currentFile = self.playlist.get_previous_track()
        self.play()

