#
# /musicBrainz.py
# Wills Media Server Media Metadata
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

import requests


class MusicBrainsAPI:
    def __init__(self):
        self.logger = logging.getLogger("wms.external-api.musicbrainz")

    def get(self, songName, songArtist=""):
        url = "http://musicbrainz.org/ws/2/release?fmt=json&query=release:{}".format(
            songName)
        if songArtist != "":
            url = url + " AND artist:{}".format(songArtist)

        request = requests.get(url)
        if request.status_code == 200:
            result = request.json()
            song = result["releases"][0]
            metadata = {
                "name": str(song["title"]),
                "artist_mbid": str(song["artist-credit"][0]["artist"]["id"]),
                "album_mbid": str(song["release-group"]["id"]),
                "song_mbid": str(song["id"])
            }

            return metadata
        else:
            self.logger.warning(
                "Failed to get metadata on {} by {}".format(songName, songArtist))
            return None


mbapi = MusicBrainsAPI()
print(mbapi.get("", ""))
