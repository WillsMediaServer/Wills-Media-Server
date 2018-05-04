#
# /wms/api/apiBlueprintV1.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

from flask import Blueprint
import logging

from wms.api.v1 import musicAPI

class api:
    def __init__(self, database):
        self.logger = logging.getLogger('wms.api')
        self.api = Blueprint("apiV1", __name__, url_prefix='/api/v1')
        self.main(self.api, database)

    def main(self, api, database):
        musicAPI.Music(api, database)
