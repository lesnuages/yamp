import sys, os, thread
import pygst
pygst.require('0.10')
import gst
from hsaudiotag import auto
from playlist import Playlist, Song

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
        self.currentSong = None

    def get_player(self):
        return self.player

    def is_playing(self):
        return self.playing

    def set_current_file(self,cfile):
        self.currentFile = cfile

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message, song=None):
        for obs in self.observers:
            obs.update(message, song)

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
            tmplist = list()
            for filepath in pl:
                infos = self.get_file_infos(filepath)
                tmplist.append(Song(infos["title"],infos["artist"],infos["album"],infos["track_number"],filepath))
            self.playlist = Playlist("New Playlist", tmplist)
            self.currentSong = self.playlist.get_current()
            self.currentFile = self.currentSong.get_path()
            self.notify_observers("update_playlist")

    def open_file(self):
        self.player.set_property("uri", "file://" + self.currentFile)

    def play(self, song=None):
        if song is not None:
            self.playlist.set_current(song)
            self.currentFile = song.get_path()
            self.currentSong = song

        if self.currentFile is not None:
            self.currentFile = self.currentSong.get_path()
            if not self.is_playing():
                self.open_file()
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
            self.notify_observers("play", self.currentSong)

    def get_file_infos(self,sfile):
        if sfile is not None:
            mfile = auto.File(sfile)
            fileInfos = dict()
            fileInfos.update({"artist":mfile.artist, "album":mfile.album, "title":mfile.title, "track_number":mfile.track})
            return fileInfos

    def get_playlist(self):
        return self.playlist

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.playing = False
        self.notify_observers("pause")

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.notify_observers("reset")
        self.playing = False

    def play_next(self):
        if self.is_playing():
            self.stop()
            self.currentSong = self.playlist.get_next_track()
            self.play()

    def play_prev(self):
        if self.is_playing():
            self.stop()
            self.currentSong = self.playlist.get_previous_track()
            self.play()

