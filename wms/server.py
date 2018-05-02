#
# /wms/server.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import atexit, logging, sys, os
from gevent.wsgi import WSGIServer

from wms import BASE_DIR
from wms.hooks import Hooks
from wms.database import db

class Server:
    def __init__(self, app):
        self.logger = logging.getLogger('wms.core')
        self.start(app)

    def start(self, app):
        # setup default wms logger
        self.logger.info("===== WMS is Starting =====")

        # init stop function
        atexit.register(self.stop)

        # Apply WMS-Core hooks
        Hooks(app)

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
        self.logger.info("Starting WMS Server")

        try:
            self.server = WSGIServer(('', 80), app).serve_forever()
        except KeyboardInterrupt:
            sys.exit()


    def stop(self):
        self.logger.info("===== Shutting Down WMS =====")
