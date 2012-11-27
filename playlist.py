class Playlist(list):
    def __init__(self, name=None, filelist=None):
        list.__init__(self)
        self._name = name
        self._current_index = 0
        if filelist is not None:
            self.extend(filelist)

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
