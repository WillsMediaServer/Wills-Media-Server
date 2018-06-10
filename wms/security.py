#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/security.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

import libraries.wmsCertGen


class Security:
    def __init__(self, config, SECURITY_DIR):
        self.logger = logging.getLogger("wms.security")
        self.logger.info("starting Security")
        httpsSetting = config.get("https", "false")
        if httpsSetting == "true":
            self.logger.info("HTTPS enabled")
            self.cert = libraries.wmsCertGen.CertGen(config, SECURITY_DIR)
