#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/api/v1/musicAPI.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import base64
import datetime
import logging
import os

from flask import jsonify, request

from mediaSearcher import Searcher
from wms import STATIC_DIR
from wms.database import Albums, Artists, AudioImages, Genres, Songs


class Music:
    def __init__(self, api, database):
        self.logger = logging.getLogger('wms.api')
        self.libraryLogger = logging.getLogger('wms.media-library')
        self.logger.debug("Adding Music API Endpoints")
        self.getRoutes(api, database)
        self.postRoutes(api, database)

    def getRoutes(self, api, database):

        @api.route('/music/songs/', methods=['GET'])
        def songs():
            limit = request.args.get("limit", 50)
            offset = request.args.get("offset", 0)
            songList = Songs.query.offset(offset).limit(limit)
            returnData = []
            for song in songList:
                newSongData = {
                    'id': int(song.id),
                    'name': str(song.name),
                    'length': str(song.length),
                    'location': str(song.location),
                    'artist': {
                        'id': int(song.artist.id),
                        'name': str(song.artist.name)
                    },
                    'album': {
                        'id': int(song.album.id),
                        'name': str(song.album.name)
                    },
                    'image': {
                        'id': int(song.image.id)
                    }
                }
                returnData.append(newSongData)
            return jsonify(status="OK", result=returnData)

        @api.route('/music/songs/<int:id>', methods=['GET'])
        def songId(id):
            song = Songs.query.filter_by(id=int(id)).first()
            if song != None:
                returnData = {
                    'id': int(song.id),
                    'name': str(song.name),
                    'length': str(song.length),
                    'location': str(song.location),
                    'artist': {
                        'id': int(song.artist.id),
                        'name': str(song.artist.name)
                    },
                    'album': {
                        'id': int(song.album.id),
                        'name': str(song.album.name)
                    },
                    'image': {
                        'id': int(song.image.id)
                    }
                }
                return jsonify(status="OK", result=returnData)
            else:
                return jsonify(status="ERROR", error="Song with ID: {} does NOT exist".format(id))

        @api.route('/music/artists/', methods=['GET'])
        def artists():
            artistList = Artists.query.all()
            returnData = []
            for artist in artistList:
                newArtistData = {
                    'id': int(artist.id),
                    'name': str(artist.name),
                    'description': str(artist.description),
                    'albums': [],
                    'songs': []
                }
                for album in artist.albums:
                    newArtistData["albums"].append(int(album.id))
                for song in artist.songs:
                    newArtistData["songs"].append(int(song.id))
                returnData.append(newArtistData)
            return jsonify(status="OK", result=returnData)

        @api.route('/music/artists/<int:id>', methods=['GET'])
        def artistId(id):
            artist = Artists.query.filter_by(id=id).first()
            if artist != None:
                returnData = {
                    'id': int(artist.id),
                    'name': str(artist.name),
                    'description': str(artist.description),
                    'albums': [],
                    'songs': []
                }
                for album in artist.albums:
                    returnData["albums"].append(int(album.id))
                for song in artist.songs:
                    returnData["songs"].append(int(song.id))
                return jsonify(status="OK", result=returnData)
            else:
                return jsonify(status="ERROR", error="Artist with ID: {} does NOT exist".format(id))

        @api.route('/music/albums/', methods=['GET'])
        def albums():
            return "OK"

        @api.route('/music/albums/<int:id>', methods=['GET'])
        def albumId(id):
            return jsonify(id=str(id), status="OK")

        @api.route('/music/genres/', methods=['GET'])
        def genres():
            return "OK"

        @api.route('/music/genres/<int:id>', methods=['GET'])
        def genreId(id):
            return jsonify(id=str(id), status="OK")

        @api.route('/music/library/update/', methods=['GET'])
        def updateLibrary():

            if Albums.query.filter_by(id=1).first() == None:
                newAlbum = Albums(name="Unknown Album",
                                  artistId=1, genreId=1, imageId=1)
                self.libraryLogger.info("Adding Unknown Album placeholder")
                database.session.add(newAlbum)

            if Artists.query.filter_by(id=1).first() == None:
                newArtist = Artists(name="Unknown Artist")
                self.libraryLogger.info("Adding Unknown Artist placeholder")
                database.session.add(newArtist)

            if AudioImages.query.filter_by(id=1).first() == None:
                with open(os.path.join(STATIC_DIR, "img", "blankAudio.png"), "rb") as imageFile:
                    base64Image = base64.b64encode(imageFile.read())
                newImage = AudioImages(image=base64Image)
                self.libraryLogger.info(
                    "Adding Unknown Audio Image placeholder")
                database.session.add(newImage)

            if Genres.query.filter_by(id=1).first() == None:
                newGenre = Genres(name="Unknown Genre")
                self.libraryLogger.info("Adding Unknown Genre placeholder")
                database.session.add(newGenre)

            searcher = Searcher("music", ["E:\Music"])
            fileList = searcher.mediaResult
            tempLength = datetime.time(second=0)
            songNum = 0
            for file in fileList:
                tempName = os.path.basename(file).rsplit(".", 1)[0]
                checkData = Songs.query.filter_by(location=file).first()
                if checkData == None:
                    newSong = Songs(name=tempName, albumId=1, artistId=1,
                                    length=tempLength, location=file, imageId=1)
                    database.session.add(newSong)
                    songNum = songNum + 1
                    self.libraryLogger.debug(
                        "Adding song name: {} Number: {}".format(tempName, songNum))
                else:
                    self.libraryLogger.debug(
                        "Song name: {} already exists".format(tempName))

            self.libraryLogger.info("Adding {} songs".format(songNum))
            database.session.commit()
            return jsonify(status="OK", songsAdded=songNum)

    def postRoutes(self, api, database):
        pass
