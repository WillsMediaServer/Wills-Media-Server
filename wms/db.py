import logging

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class ServerSettings(db.Model):
    __bind_key__ = "main"
    __tablename__ = "serverSettings"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(64))
    category = db.Column("category", db.String(64))
    value = db.Column("value", db.Text)
    description = db.Column("description", db.Text)

# Tables for the Users Database
class User(db.Model):
    __bind_key__ = "users"
    __tablename__ = "user"
    id = db.Column("userID", db.Integer, primary_key=True)
    username = db.Column("username", db.String(255), unique=True)
    password = db.Column("password", db.String(255))
    firstName = db.Column("firstName", db.String(255))
    lastName = db.Column("lastName", db.String(255))
    fullName = db.column_property(firstName + " " + lastName)
    email = db.Column("email", db.String(255), unique=True)
    permission = db.Column("permission", db.Integer)

# tables for the Music Database

class Artists(db.Model):
    __bind_key__ = "music"
    __tablename__ = "artists"
    id = db.Column("artistID", db.Integer, primary_key=True)
    name = db.Column("name", db.String(255))
    description = db.Column("description", db.TEXT)

class Albums(db.Model):
    __bind_key__ = "music"
    __tablename__ = "albums"
    id = db.Column("albumID", db.Integer, primary_key=True)
    artistId = db.Column("artistID", db.Integer)
    name = db.Column("name", db.String(255))
    releaseDate = db.Column("releaseDate", db.DATE)
    genreId =
    picture

class Songs(db.Model):
    __bind_key__ = "music"
    __tablename__ = "songs"
    id = db.Column("songID", db.Integer, primary_key=True)
    albumId = db.Column("albumID", db.Integer)
