#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/__init__.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

# import needed modules from the stdlib
import datetime
import logging
import os
import sys
from logging.config import dictConfig

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
    from flask import Flask
    from wms.server import Server

    # Initialize Flask
    app = Flask(__name__)
    app.debug = False

    # remove werkzeug logger again
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.disabled = True

    server = Server(app)
