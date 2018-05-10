#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/server.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging
import os
import sys

from flask import jsonify, render_template

from gevent.wsgi import WSGIServer
from wms import BASE_DIR, LIB_DIR, clientBlueprint
from wms.api import apiBlueprintV1
from wms.hooks import Hooks
from wms.media import covers, music


class Server:
    def __init__(self, app, db, config):
        self.logger = logging.getLogger('wms.core')
        self.logger.info("===== WMS is Starting =====")
        self.config = config

        # Add error pages
        @app.errorhandler(404)
        def error404(error):
            return jsonify(error="Error 404", details=str(error)), 404

        @app.errorhandler(500)
        def error500(error):
            return jsonify(error="Error 500", details=str(error)), 500

        self.start(app, db)

    def start(self, app, db):
        # Apply WMS-Core hooks
        Hooks(app)

        # Add base API Blueprint

        apiV1 = apiBlueprintV1.api(db)
        webClientBP = clientBlueprint.WebClient(db)
        mediaCovers = covers.Covers(db)
        mediaMusic = music.Song(db)
        app.register_blueprint(apiV1.api)
        app.register_blueprint(webClientBP.webClient)
        app.register_blueprint(mediaCovers.covers)
        app.register_blueprint(mediaMusic.song)

        # Start the server and prevent gevent from logging requests as they're already handled.
        self.server = WSGIServer((self.config.get("host", "0.0.0.0"), int(
            self.config.get("port", "80"))), application=app, log=None)

        try:
            self.logger.info("Starting WMS Server")
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.logger.info("===== Shutting Down WMS =====")
        self.server.stop()
        sys.exit()
