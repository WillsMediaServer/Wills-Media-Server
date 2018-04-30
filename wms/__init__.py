#
# /wms/__init__.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

# import needed modules from the stdlib
import sys, os, logging, threading, time

# create a handy BASE_DIR variable
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# and use it to insert the libraries folder to the path
sys.path.insert(1, os.path.join(BASE_DIR, "libraries"))
# which allows for imports from the libraries folder

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask.logging as flaskLogging
from logging.config import dictConfig

from wms.database import db
from wms.hooks import Hooks

# Initialize Flask
app = Flask(__name__, instance_relative_config=True)
app.debug = True

# Disable default logs
werkzeugLog = logging.getLogger('werkzeug')
werkzeugLog.disabled = True
# app.logger.disabled = True

# Init logging
file_location = os.path.join(BASE_DIR, "logs", "main.log")
dictConfig({
    'version':1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] [%(section)s] %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_location,
            'maxBytes': 16384,
            'backupCount': 10,
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'datefmt': '%d-%m-%Y %H:%M:%S',
        'handlers': ['file', 'stdout']
    }
})

mainLogger = logging.getLogger("root")
logger = logging.LoggerAdapter(mainLogger, {"section":"WMS-Core"})

def start(app):
    logger.info("\n"+("="*25)+"\n\n  WMS-Core is Starting  \n\n"+("="*25))
    # Apply WMS-Core hooks
    Hooks(app, mainLogger)

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = str("sqlite:///" + os.path.join(BASE_DIR, "database", "main.db"))
    app.config["SQLALCHEMY_BINDS"] = {
        "users": str('sqlite:///' + os.path.join(BASE_DIR, "database", "users.db")),
        "music": str('sqlite:///' + os.path.join(BASE_DIR, "database", "music.db")),
        "films": str('sqlite:///' + os.path.join(BASE_DIR, "database", "films.db")),
        "tv": str('sqlite:///' + os.path.join(BASE_DIR, "database", "tv.db"))
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy Databases
    db.init_app(app)
    db.create_all(app=app)

    from wms.api import apiBlueprintV1
    apiV1 = apiBlueprintV1.api(db)
    app.register_blueprint(apiV1.api)
    logger.info("Starting WMS Server")

start(app)
