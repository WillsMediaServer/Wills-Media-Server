import os, logging

class Search:
    def __init__(self, paths, supportedExt=[".mp3", ".wav", ".ogg", ".m4a"]):
        paths = paths[0].split(",")
        songs = []
        for path in paths:
            for dir, subdir, files in os.walk(path):
                for file in files:
                    for ext in supportedExt:
                        if file.lower().endswith(ext):
                            songs.append(os.path.join(dir,file))
        self.songs = songs
