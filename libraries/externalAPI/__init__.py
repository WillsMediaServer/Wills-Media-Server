#
# /__init__.py
# Wills Media Server External APIs
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

from .musicBrainz import MusicBrainsAPI


class ExternalAPI:
    def __init__(self):
        self.logger = logging.getLogger("wms.external-api")
        self.logger.info("Starting External APIs")
        self.MusicBrainsAPI = MusicBrainsAPI
