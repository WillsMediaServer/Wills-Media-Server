import logging, random
from wms import config, db

class Server:
    def __init__(self, app, config):
        logging.info("Initialising Server")
        self.configData = config.configData
        self.runServer(app)

    def runServer(self, app):
        app.secret_key = self.configData["Security"]["salt"]
        host = self.configData["Server"]["hostname"]
        port = int(self.configData["Server"]["port"])
        app.run(host=host, port=port, threaded=True)
