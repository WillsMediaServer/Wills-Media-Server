#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/clientBlueprint.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging
import os

from flask import Blueprint

from wms import LIB_DIR


class WebClient:
    def __init__(self, database):
        self.logger = logging.getLogger('wms.client')
        self.webClient = Blueprint(
            "webClient", __name__, url_prefix='/', static_url_path='/assets', static_folder=os.path.join(LIB_DIR, "WMS-UI", "build", "assets"))
        self.main(self.webClient, database)

    def main(self, webClient, database):
        @webClient.route('/')
        def webClient():
            with open(os.path.join(LIB_DIR, "WMS-UI", "build", "index.html"), 'r') as webClientFile:
                webClientHTML = webClientFile.read()
            return str(webClientHTML)
