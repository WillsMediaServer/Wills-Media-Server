#
# /musicBrainz.py
# Wills Media Server Media Metadata
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

import musicbrainzngs


class MusicBrainsAPI:
    def __init__(self):
        self.logger = logging.getLogger("wms.external-api.musicbrainz")
        musicbrainzngs.set_useragent("WillsMediaServer", "v0.0.1.0 ALPHA")

    def get_song(self, songName, songArtists):
        if songArtists != "":
            results = musicbrainzngs.search_releases(
                release=songName, artist=songArtists)
        else:
            results = musicbrainzngs.search_releases(release=songName)
        return results["release-list"][0]
