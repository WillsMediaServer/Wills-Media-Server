#
# /wms/database.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import logging

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Server settings table
class ServerSettings(db.Model):
    __bind_key__ = "main"
    __tablename__ = "serverSettings"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64))
    category = db.Column("category", db.String(64))
    value = db.Column("value", db.Text)
    description = db.Column("description", db.Text)
