import logging
import os

from flask import Blueprint, Response, jsonify, send_file, stream_with_context
from werkzeug.datastructures import Headers

from wms.database import Songs


class Song:
    def __init__(self, database):
        self.logger = logging.getLogger('wms.media.song')
        self.song = Blueprint("song", __name__, url_prefix='/media/song')
        self.supportedExtensions = ["mp3", "wav",
                                    "ogg", "m4a", "flac", "aac", "wma"]
        self.supportedMimes = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "ogg": "audio/ogg",
            "m4a": "audio/m4a",
            "flac": "audio/flac",
            "aac": "audio/aac",
            "wma": "audio/x-ms-wma"
        }
        self.main(self.song, database)

    def main(self, song, database):
        @song.route('/<int:id>')
        def getSong(id):
            song = Songs.query.filter_by(id=id).first()
            if song != None:
                try:
                    songLocation = song.location
                    for extension in self.supportedExtensions:
                        if songLocation.lower().endswith(extension):
                            songMime = self.supportedMimes[extension]
                            break
                        else:
                            songMime = "audio/*"
                    headers = Headers()
                    headers.add("Content-Transfer-Encoding", "binary")
                    headers.add("Content-Disposition", "inline",
                                filename=song.name.encode('ascii', 'ignore'))
                    headers.add("Content-length",
                                os.path.getsize(songLocation))
                    headers.add("Accept-Ranges", "bytes")

                    def generate():
                        with open(songLocation, "rb") as audio:
                            data = audio.read(1024)
                            while data:
                                yield data
                                data = audio.read(1024)
                    return Response(stream_with_context(generate()), mimetype=songMime, headers=headers)
                except FileNotFoundError as error:
                    self.logger.warning(
                        "File Not Found: {}".format(song.location))
                    return jsonify(status="error", error=str(error))
                except Exception as error:
                    return jsonify(status="error", error=str(error))
            else:
                return jsonify(status="error", error="Song doesn't exist")
