
class Playlist():
    def __init__(self, name=None, filelist=None):
        self._name = name
        self._files = filelist
        self._len = len(filelist)

