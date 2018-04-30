import logging
from flask import Flask, request

class Hooks:
    def __init__(self, app, mainLogger):
        self.logger = logging.LoggerAdapter(mainLogger, {"section":"Hooks"})
        self.serverLogger = logging.LoggerAdapter(mainLogger, {"section":"Server"})
        self.logger.info("Adding WMS-Core Hooks")
        self.main(app)

    def main(self, app):
        self.logger.info("Adding After Request Hook")
        @app.after_request
        def after_request(response):
            responseLogFormat = "{} {} {} \"{}\" {}".format(request.remote_addr, request.method, response.status, response.mimetype, request.path)
            self.serverLogger.info(responseLogFormat)
            response.headers["Server"] = "Wills Media Server v0.0.1"
            return response
