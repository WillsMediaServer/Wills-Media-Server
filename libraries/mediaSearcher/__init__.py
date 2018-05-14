#
# /__init__.py
# Wills Media Server Media Searcher
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging
import os

supportedExtensions = {
    "music": ["mp3", "wav", "ogg", "m4a", "flac", "aac", "wma"],
    "films": [],
    "tv": []
}


class Searcher:
    def __init__(self, mediaType, paths=[]):
        self.logger = logging.getLogger('wms.media-searcher')
        self.mediaResult = []
        if mediaType == "music":
            self.mediaResult = self.music(paths)
        elif mediaType == "films":
            self.mediaResult = self.films(paths)
        elif mediaType == "tv":
            self.mediaResult = self.tv(paths)
        else:
            self.logger.error("Media Type doesn't exist")

        if self.mediaResult == []:
            self.logger.error("Media Searcher found no supported media files")

    def music(self, paths):
        songs = []
        if (paths[0] != None) or (paths[0] == ""):
            for path in paths:
                for dir, subdir, files in os.walk(path):
                    for filename in files:
                        for extension in supportedExtensions["music"]:
                            if filename.lower().endswith(extension):
                                songs.append(os.path.join(dir, filename))
        else:
            self.logger.info("No Path is set for music")
        return songs

    def films(self, paths):
        pass

    def tv(self, paths):
        pass
