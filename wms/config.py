#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/config.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

from wms.database import ServerSettings


class Config:
    def __init__(self, app, database):
        self.logger = logging.getLogger('wms.config')
        self.logger.info("Loading Config")
        self.app = app
        self.database = database

    def get(self, name, backup=""):
        with self.app.app_context():
            option = ServerSettings.query.filter_by(name=name).first()
            if option == None:
                self.logger.warning(
                    "{} doesn't exist, now setting with default value".format(name))
                self.set(name, backup)
            else:
                return option.value

    def set(self, name, value=""):
        with self.app.app_context():
            self.logger.info("Setting {} to {}".format(name, value))
            newSetting = ServerSettings(
                name=name, category=None, value=value, description=None)
            self.database.session.add(newSetting)
            self.database.session.commit()
