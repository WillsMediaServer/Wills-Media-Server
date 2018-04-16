from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, abspath, normpath
import mutagen
import db

BASE_DIR = r"B:/WMS/WMS-Core/"

database = db.db
Songs = db.Songs

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = str("sqlite:///" + join(BASE_DIR, "database", "main.db"))
app.config["SQLALCHEMY_BINDS"] = {
    "users": str('sqlite:///' + join(BASE_DIR, "database", "users.db")),
    "music": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "music.db")),
    "films": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "films.db")),
    "tv": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "tv.db"))
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
def testPage():
    song = Songs.query.all()[0]
    audioFile = mutagen.File(song.location)
    print(audioFile)
    # songsList = Songs.query.all()
    # for song in songsList:
    #     location = song.location
    #     audioFile = mutagen.File(location)
    #     print(dir(audioFile))
    return "Hello World"

database.init_app(app)
database.create_all(app=app)
app.run(host="0.0.0.0", port=8080, threaded=True)
