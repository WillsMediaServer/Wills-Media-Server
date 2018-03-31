from flask import Blueprint, render_template, request, session, redirect, Response, stream_with_context, make_response
from werkzeug.datastructures import Headers
from wms.music import Search

import os, datetime, logging

class musicBlueprint:
    def __init__(self, config, database, security):
        self.music = Blueprint("music", __name__, url_prefix='/music')
        self.main(self.music, config, database, security)

    def main(self, music, config, database, security):
        self.configData = config.configData

        @music.route("/")
        def musicHomePage():
            songsList = database.Songs.query.all()
            pageConfig = security.pageData(self.configData, database)
            return render_template("music/music.html", pageName="Music", config=pageConfig, songs=songsList)

        @music.route("/update")
        def updateMusicLibrary():
            paths = []
            paths.append(os.path.abspath(self.configData["Media"]["musicpath"]))
            print(paths)
            data = Search(paths)
            songs = data.songs
            for songPath in songs:
                logging.debug("Checking song at: " + songPath)
                checkData = database.Songs.query.filter_by(location=songPath).first()
                if checkData == None:
                    name = os.path.basename(songPath).rsplit(".",1)[0]
                    item = database.Songs(name=name,album=1,artist=1,length=datetime.time(second=0),location=songPath)
                    database.db.session.add(item)
                    logging.debug("Adding Song: " + name)
                else:
                    logging.debug("Song Already exists. Skipping...")
            database.db.session.commit()
            return "OK"

        @music.route("/get/song/<int:id>")
        def getSong(id):
            songData = database.Songs.query.filter_by(id=id).first()
            if songData == None:
                return render_template("music/noExist.html", pageName="Song Doesn't Exist", config=pageConfig)
            else:
                songLocation = songData.location
                headers = Headers()
                headers.add("Content-Transfer-Encoding", "binary")
                headers.add("Content-Disposition", "inline", filename=songData.name)
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
