#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/security.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging


class Security:
    def __init__(self, config):
        self.logger = logging.getLogger("wms.security")
        self.logger.info("starting Security")
