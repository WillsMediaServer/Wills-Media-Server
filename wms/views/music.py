from flask import Blueprint, render_template, request, session, redirect, Response, stream_with_context, make_response, send_file
from werkzeug.datastructures import Headers
from wms.music import Search

import os, datetime, logging, base64, io, sys, json
from os.path import join, dirname, abspath, normpath
BASE_DIR = normpath(join(dirname(abspath(__file__)), "..", ".."))

sys.path.insert(1, join(BASE_DIR, "libs"))

from ffmpegWrapper.wrapper import Wrapper
ffmpeg = Wrapper()

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

        @music.route("/update/library")
        def updateMusicLibrary():
            paths = []
            paths.append(os.path.abspath(self.configData["Media"]["musicpath"]))
            data = Search(paths)
            songs = data.songs
            for songPath in songs:
                logging.debug("Checking song at: " + songPath)
                checkData = database.Songs.query.filter_by(location=songPath).first()
                if checkData == None:
                    name = os.path.basename(songPath).rsplit(".",1)[0]
                    item = database.Songs(name=name,albumId=1,artistId=1,length=datetime.time(second=0),location=songPath, imageId=1)
                    database.db.session.add(item)
                    logging.debug("Adding Song: " + name)
                else:
                    logging.debug("Song Already exists. Skipping...")
            if database.AudioImages.query.filter_by(id=1).first() == None:
                with open(join(BASE_DIR, "wms", "static", "img", "blankAudio.png"), "rb") as imageFile:
                    base64Image = base64.b64encode(imageFile.read())
                image = database.AudioImages(image=base64Image)
                database.db.session.add(image)
            if database.Genres.query.filter_by(id=1).first() == None:
                genere = database.Genres(name="Unknown Genre")
                database.db.session.add(genere)
            if database.Artists.query.filter_by(id=1).first() == None:
                artist = database.Artists(name="Unknown Artist")
                database.db.session.add(artist)
            if database.Albums.query.filter_by(id=1).first() == None:
                album = database.Albums(name="Unknown Album", artistId=1, genreId=1, imageId=1)
                database.db.session.add(album)
            database.db.session.commit()
            return "OK"

        @music.route("/update/metadata")
        def updateMusicMetadata():
            songs = database.Songs.query.all()
            for song in songs:
                id = song.id
                location = song.location
                metadata = json.loads(ffmpeg.metadata(location, ["title", "artist", "album"]))
                if metadata["title"] != None:
                    song.name = metadata["title"]

                if metadata["artist"] != None:
                    artistExistCheck = database.Artists.query.filter_by(name=metadata["artist"]).first()
                    if artistExistCheck == None:
                        artistNames = metadata["artist"].split(";")
                        artistIds = []
                        for artistName in artistNames:
                            artist = database.Artists(name=artistName.lstrip())
                            database.db.session.add(artist)
                        database.db.session.commit()
                        for artistName in artistNames:
                            artist = database.Artists.query.filter_by(name=artistName.lstrip()).first()
                            if artist != None:
                                artistIds.append(artist.id)
                        song.artistId = artistIds[0]
                    if artistExistCheck != None:
                        if song.artistId != artistExistCheck.id:
                            song.artistId = artistExistCheck.id

                if metadata["album"] != None:
                    pass
                database.db.session.commit()
            return "OK"

        @music.route("/get/img/<int:imgId>")
        def getImage(imgId):
            audioImage = database.AudioImages.query.filter_by(id=imgId).first()
            if audioImage == None:
                filename = join(BASE_DIR, "wms", "static", "img", "blankAudio.png")
                return send_file(filename, mimetype="image/png")
            else:
                image = base64.b64decode(audioImage.image)
                return send_file(io.BytesIO(image), mimetype="image/png", as_attachment=False)

        @music.route("/get/song/<int:id>")
        def getSong(id):
            songData = database.Songs.query.filter_by(id=id).first_or_404()
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
            songData = database.Songs.query.filter_by(id=id).first_or_404()
            pageConfig = security.pageData(self.configData, database)
            return render_template("music/play.html", pageName="Music", config=pageConfig, id=id, song=songData, loadJS=["musicPlayer.js"])
