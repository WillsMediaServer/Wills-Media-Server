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

from flask import jsonify

from gevent.wsgi import WSGIServer
from wms import BASE_DIR
from wms.database import db
from wms.hooks import Hooks


class Server:
    def __init__(self, app):
        self.logger = logging.getLogger('wms.core')
        self.logger.info("===== WMS is Starting =====")

        # Add error pages
        @app.errorhandler(404)
        def error404(error):
            return jsonify(error="Error 404", details=str(error)), 404

        @app.errorhandler(500)
        def error500(error):
            return jsonify(error="Error 500", details=str(error)), 500

        self.start(app)

    def start(self, app):
        # Apply WMS-Core hooks
        Hooks(app)

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

        # Add base API Blueprint
        from wms.api import apiBlueprintV1
        apiV1 = apiBlueprintV1.api(db)
        app.register_blueprint(apiV1.api)

        # Start the server and prevent gevent from logging requests as they're already handled.
        self.server = WSGIServer(("0.0.0.0", 80), application=app, log=None)

        try:
            self.logger.info("Starting WMS Server")
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.logger.info("===== Shutting Down WMS =====")
        self.server.stop()
        sys.exit()
