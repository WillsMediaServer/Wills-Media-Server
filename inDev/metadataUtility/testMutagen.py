from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, abspath, normpath
from wmsMeta.meta import meta
import mutagen, sys

BASE_DIR = normpath(join(dirname(abspath(__file__)), "..", ".."))
sys.path.insert(1, join(BASE_DIR, "wms"))

import db

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
    songs = Songs.query.all()
    data = []
    for song in songs:
        metadata = meta(song.location, ["title", "artist", "track", "album"])
        data.append(metadata)
    return str(data)

database.init_app(app)
database.create_all(app=app)
app.run(host="0.0.0.0", port=8080, threaded=True)
