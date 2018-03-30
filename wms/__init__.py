# Will's Media Server
# wms/__init__.py
# By William Neild

# Setup libraries
import sys
from os.path import join, dirname, abspath, normpath
sys.path.insert(1, "./libs/")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set BASE_DIR variable
BASE_DIR = normpath(join(dirname(abspath(__file__)), ".."))

# grab all files/modules needed for wms
from wms import db
from wms.config import Config
from wms.security import Security
from wms.server import Server
import logging, sys, time

database = db

# Setup logging to both file and terminal
try:
    file_location = join(BASE_DIR, "logs", "main.log")
    print("Logs file stored at: " + str(file_location))
    file_handler = logging.FileHandler(filename=str(file_location))
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]
    logging.basicConfig(
        level = logging.DEBUG,
        format = "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt = "%d-%m-%Y %H:%M:%S",
        handlers = handlers
    )
except Exception as error:
    print("Error: " + str(error))
    sys.exit()

# Initialise flask
app = Flask(__name__)

# configure sqlalchemy withy flask
app.config["SQLALCHEMY_DATABASE_URI"] = str("sqlite:///" + join(BASE_DIR, "database", "main.db"))
app.config["SQLALCHEMY_BINDS"] = {
    "users": str('sqlite:///' + join(BASE_DIR, "database", "users.db")),
    "music": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "music.db")),
    "films": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "films.db")),
    "tv": str('sqlite:///' + join(BASE_DIR, "database", "libraries", "tv.db"))
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Load Required core config
config = Config()
security = Security(config)

# Add all flask views
from .views import home, dashboard, music, films, tv
homeBlueprint = home.homeBlueprint(config, database, security)
dashboardBlueprint = dashboard.dashboardBlueprint(config, database, security)
musicBlueprint = music.musicBlueprint(config, database, security)
filmsBlueprint = films.filmsBlueprint(config, database, security)
tvBlueprint = tv.tvBlueprint(config, database, security)

# Register Flask Blueprints
app.register_blueprint(homeBlueprint.home)
app.register_blueprint(dashboardBlueprint.dashboard)
app.register_blueprint(musicBlueprint.music)
app.register_blueprint(filmsBlueprint.films)
app.register_blueprint(tvBlueprint.tv)

# Initialise SQLAlchemy Databases
database.db.init_app(app)
database.db.create_all(app=app)

# Start the Web UI
server = Server(app, config)
