#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/__init__.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

"""Wills Media Server

This module is Wills Media Server and holds the API and all of the media/metadata
handling and storing.

"""

# import needed modules from the stdlib
import datetime
import logging
import os
import sys
from logging.config import dictConfig

from wms.config import Config
from wms.database import db

# create a handy BASE_DIR variable
BASE_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
STATIC_DIR = os.path.join(BASE_DIR, "wms", "static")
LIB_DIR = os.path.join(BASE_DIR, "libraries")
# and use it to insert the libraries folder to the path
sys.path.insert(1, LIB_DIR)
# which allows for imports from the libraries folder

logfile = os.path.join(
    LOG_DIR, datetime.datetime.now().strftime('%Y-%m-%d') + ".main.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

i = 0
if os.path.exists(logfile):
    while True:
        i += 1
        if not os.path.exists(logfile + "." + str(i)):
            os.rename(logfile, logfile + "." + str(i))
            break

# Init logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': logfile,
            'formatter': 'default'
        }
    },
    'root': {
        'level': logging.DEBUG,
        'datefmt': '%d-%m-%Y %H:%M:%S',
        'handlers': ['file', 'stdout']
    },
    'werkzeug': {
        'level': logging.ERROR,
        'datefmt': '%d-%m-%Y %H:%M:%S',
        'handlers': ['file', 'stdout']
    },
    'flask.app': {
        'level': logging.ERROR,
        'datefmt': '%d-%m-%Y %H:%M:%S',
        'handlers': ['file', 'stdout']
    }
})


def init():
    """Initialize WMS

    This function creates the flask app, disables the werkzeug logger and then it
    initializes the Server class to start the server.

    """
    from flask import Flask
    from wms.server import Server

    # Initialize Flask
    app = Flask(__name__)
    app.debug = False

    # remove werkzeug logger again
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.disabled = True

    if not os.path.exists(os.path.join(LIB_DIR, "WMS-UI", "build")):
        logging.critical(
            "WMS-UI build doesnt exist. please clone the wms-ui repo and build it in the libraries folder")
        logging.info("Now Exiting")
        sys.exit()

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_BINDS"] = {
        "main": str("sqlite:///" + os.path.join(BASE_DIR, "database", "main.db")),
        "users": str('sqlite:///' + os.path.join(BASE_DIR, "database", "users.db")),
        "music": str('sqlite:///' + os.path.join(BASE_DIR, "database", "music.db")),
        "films": str('sqlite:///' + os.path.join(BASE_DIR, "database", "films.db")),
        "tv": str('sqlite:///' + os.path.join(BASE_DIR, "database", "tv.db"))
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy Databases
    db.init_app(app)
    db.create_all(app=app)

    # Initialize Config
    config = Config(app, db)

    server = Server(app, db, config)
