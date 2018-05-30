#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/hooks.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging
import gzip

from io import BytesIO as IO

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
            # Custom logging
            responseLogFormat = "{} {} {} \"{}\" {}".format(
                request.remote_addr, request.method, response.status, response.mimetype, request.path)
            self.serverLogger.info(responseLogFormat)
            # Custom headers
            response.headers["Server"] = "Wills Media Server v0.0.1"
            response.headers["Access-Control-Allow-Origin"] = "*"
            # GZip all requests
            accept_encoding = request.headers.get('Accept-Encoding', '')
            if 'gzip' not in accept_encoding.lower():
                pass
            else:
                response.direct_passthrough = False

                if (response.status_code < 200 or response.status_code >= 300 or 'Content-Encoding' in response.headers):
                    return response
                gzip_buffer = IO()
                gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
                gzip_file.write(response.data)
                gzip_file.close()

                response.data = gzip_buffer.getvalue()
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'
                response.headers['Content-Length'] = len(response.data)

            return response
