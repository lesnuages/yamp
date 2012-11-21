import sys, os
import pygst
pygst.require('0.10')
import gst

class MusicPlayer:

    def __init__(self):
        self.observers = list()
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink",fakesink)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        self.playlist = None

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, message):
        for obs in self.observers:
            obs.update(message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.notify_observers("reset")
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print ("Error {} {}".format(err, debug))
            self.notify_observers("reset")

    def open_file(self,musicFile):
        self.player.set_property("uri", "file://" + musicFile)

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)
        self.notify_observers("play")

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
        self.notify_observers("pause")

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.notify_observers("reset")

    def play_next(self):
        self.stop()
        print("NEXT !")

    def play_prev(self):
        self.stop()
        print("PREVIOUS !")

