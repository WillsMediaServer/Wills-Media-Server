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

import cherrypy
from wms import BASE_DIR, LIB_DIR, clientBlueprint
from wms.api import apiBlueprintV1
from wms.hooks import Hooks
from wms.media import covers, music


class Server:
    def __init__(self, app, db, config, security):
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

        self.setup(app, db)

    def setup(self, app, db):
        # Apply WMS-Core hooks
        Hooks(app)

        # Add base API Blueprint

        apiV1 = apiBlueprintV1.api(db, self.config)
        webClientBP = clientBlueprint.WebClient(db)
        mediaCovers = covers.Covers(db)
        mediaMusic = music.Song(db)
        app.register_blueprint(apiV1.api)
        app.register_blueprint(webClientBP.webClient)
        app.register_blueprint(mediaCovers.covers)
        app.register_blueprint(mediaMusic.song)

        self.run_server(app)

    def run_server(self, app):
        try:
            mode = sys.argv[1]
        except Exception:
            mode = "prod"

        if mode != "dev":
            cherrypy.config.update({
                'server.socket_port': int(self.config.get("port", "80")),
                'server.socket_host': self.config.get("host", "0.0.0.0"),
                'engine.autoreload.on': False,
                'checker.on': False,
                'tools.log_headers.on': False,
                'request.show_tracebacks': False,
                'request.show_mismatched_params': False,
                'log.screen': False
            })
        else:
            cherrypy.config.update({
                'server.socket_port': int(self.config.get("port", "80")),
                'server.socket_host': self.config.get("host", "0.0.0.0"),
                'engine.autoreload.on': True,
                'checker.on': True,
                'tools.log_headers.on': True,
                'request.show_tracebacks': True,
                'request.show_mismatched_params': True,
                'log.screen': False
            })

        cherrypy.tree.graft(app, '/')
        cherrypy.tree.mount(None, '/static', {'/': {
            'tools.staticdir.dir': os.path.join(app.static_folder, "WMS-WebUI"),
            'tools.staticdir.on': True,
            'tools.gzip.on': True
        }})

        try:
            if hasattr(cherrypy.engine, "signal_handler"):
                cherrypy.engine.signal_handler.subscribe()
            if hasattr(cherrypy.engine, "console_control_handler"):
                cherrypy.engine.console_control_handler.subscribe()
            cherrypy.engine.start()
            cherrypy.engine.block()
        except KeyboardInterrupt:
            self.logger.info("===== Shutting Down WMS =====")
            cherrypy.engine.stop()
            sys.exit()
