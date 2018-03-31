from flask import Blueprint, render_template, request, session, redirect, Response, stream_with_context, make_response
from werkzeug.datastructures import Headers
import os

class musicBlueprint:
    def __init__(self, config, database, security):
        self.music = Blueprint("music", __name__, url_prefix='/music')
        self.main(self.music, config, database, security)

    def main(self, music, config, database, security):
        self.configData = config.configData

        @music.route("/")
        def musicHomePage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("music/music.html", pageName="Music", config=pageConfig)

        @music.route("/get/song/<int:id>")
        def getSong(id):
            songData = database.Songs.query.filter_by(id=id).first()
            if songData == None:
                return False
            else:
                songLocation = os.path.join(songData.location, songData.filename)
                headers = Headers()
                headers.add("Content-Transfer-Encoding", "binary")
                headers.add("Content-Disposition", "inline", filename=songData.filename)
                headers.add("Content-length", os.path.getsize(songLocation))
                headers.add("Accept-Ranges", "bytes")
                def generate():
                    with open(songLocation, "rb") as audio:
                        data = audio.read(1024)
                        while data:
                            yield data
                            data = audio.read(1024)
                return Response(stream_with_context(generate()), mimetype="audio/mpeg", headers=headers)

        @music.route("/play/<int:id>")
        def playSong(id):
            songData = database.Songs.query.filter_by(id=id).first()
            pageConfig = security.pageData(self.configData, database)
            if songData == None:
                return render_template("music/noExist.html", pageName="Song Doesn't Exist", config=pageConfig)
                logging.log("Song with the id of "+id+" not Found")
            else:
                return render_template("music/play.html", pageName="Music", config=pageConfig, id=id, song=songData)
