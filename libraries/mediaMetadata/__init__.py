#
# /__init__.py
# Wills Media Server Media Metadata
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging


class Metadata:
    def __init__(self):
        self.logger = logging.getLogger('wms.media-metadata')
