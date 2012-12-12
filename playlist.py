class Playlist(list):
    def __init__(self, name=None, songList=None):
        list.__init__(self)
        self._name = name
        self._current_index = 0
        if songList is not None:
            self.extend(songList)

    def save(self, filepath):
        return None
    
    def get_previous_track(self):
        if len(self) > 0:
            if self._current_index > 0:
                self._current_index -= 1
            else:
                self._current_index = 0
        return self[self._current_index]

    def get_next_track(self):
        if len(self) > 0:
            if (self._current_index+1 >= len(self)):
                self._current_index = 0
            else:
                self._current_index += 1
        return self[self._current_index]

    def get_first(self):
        return self[0]

    def get_last(self):
        return self[len(self)-1]

    def get_current(self):
        return self[self._current_index]

    def set_current(self, song):
        for s in self:
            if s == song:
                self._current_index = self.index(s)

class Song():
    def __init__(self, stitle="Unknown", sartist="Unknown", salbum="Unknown", strack="Unknown",spath=None):
        self.title = stitle
        self.artist = sartist
        self.album = salbum
        self.track = strack
        self.path = spath

    def get_path(self):
        return self.path
    
    def get_title(self):
        return self.title

    def get_artist(self):
        return self.artist

    def get_album(self):
        return self.album

    def get_track(self):
        return self.track

    def __eq__(self,song):
        if self.artist == song.get_artist():
            if self.album == song.get_album():
                if self.title == song.get_title():
                    if str(self.track) == str(song.get_track()):
                        return True
        return False

