#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/hooks.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

from flask import Flask, request


class Hooks:
    def __init__(self, app):
        self.hooksLogger = logging.getLogger('wms.hooks')
        self.serverLogger = logging.getLogger('wms.server')
        self.hooksLogger.debug("Adding WMS-Core Hooks")
        self.main(app)

    def main(self, app):
        self.hooksLogger.debug("Adding After Request Hook")

        @app.after_request
        def after_request(response):
            responseLogFormat = "{} {} {} \"{}\" {}".format(
                request.remote_addr, request.method, response.status, response.mimetype, request.path)
            self.serverLogger.info(responseLogFormat)
            response.headers["Server"] = "Wills Media Server v0.0.1"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response
