#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/api/apiBlueprintV1.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

from flask import Blueprint

from wms.api.v1 import musicAPI


class api:
    def __init__(self, database, config):
        self.logger = logging.getLogger('wms.api')
        self.api = Blueprint("apiV1", __name__, url_prefix='/api/v1')
        self.main(self.api, database, config)

    def main(self, api, database, config):
        musicAPI.Music(api, database, config)
