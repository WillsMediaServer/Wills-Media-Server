#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /wms/api/v1/musicAPI.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import base64
import datetime
import json
import logging
import multiprocessing
import os

from flask import jsonify, request

import externalAPI
from mediaMetadata import Metadata
from mediaSearcher import Searcher
from wms import STATIC_DIR
from wms.database import Albums, Artists, AudioImages, Genres, Songs

mbapi = externalAPI.ExternalAPI().MusicBrainsAPI()


def getMetadata(data):
    name = data["name"]
    artists = data["artists"]
    print("Getting {} By {}".format(name, artists))
    return mbapi.get_song(name, artists)


class Music:
    def __init__(self, api, database, config):
        self.logger = logging.getLogger('wms.api')
        self.libraryLogger = logging.getLogger('wms.media-library')
        self.logger.debug("Adding Music API Endpoints")
        self.config = config
        self.getRoutes(api, database)
        self.postRoutes(api, database)

    def getRoutes(self, api, database):

        @api.route('/music/songs/', methods=['GET'])
        def songs():
            limit = request.args.get("limit", 1000)
            offset = request.args.get("offset", 0)
            songList = Songs.query.offset(offset).limit(limit)
            numberOfSongs = database.session.query(Songs).count()
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
            return jsonify(status="OK", result=returnData, number=numberOfSongs)

        @api.route('/music/songs/<int:id>', methods=['GET'])
        def songId(sid):
            song = Songs.query.filter_by(id=int(sid)).first()
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
                return jsonify(status="ERROR", error="Song with ID: {} does NOT exist".format(sid))

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
        def artistId(aid):
            artist = Artists.query.filter_by(id=aid).first()
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
                return jsonify(status="ERROR", error="Artist with ID: {} does NOT exist".format(aid))

        @api.route('/music/albums/', methods=['GET'])
        def albums():
            return "OK"

        @api.route('/music/albums/<int:id>', methods=['GET'])
        def albumId(aid):
            return jsonify(id=str(aid), status="OK")

        @api.route('/music/genres/', methods=['GET'])
        def genres():
            return "OK"

        @api.route('/music/genres/<int:id>', methods=['GET'])
        def genreId(gid):
            return jsonify(id=str(gid), status="OK")

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

            database.session.commit()
            paths = self.config.get("musicPaths", "").split(';')
            searcher = Searcher("music", paths)
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

        @api.route('/music/library/metadata/', methods=['GET'])
        def updateMetadata():
            metadataSearcher = Metadata()
            songList = Songs.query.all()
            for song in songList:
                path = song.location
                songMetadata = json.loads(metadataSearcher.metadata(
                    path, ["artist", "title", "album"]))
                if songMetadata["artist"] != None:
                    if song.artistId == 1:  # Check if it is an unknown artist
                        artistList = songMetadata["artist"].split(";")
                        artists = []
                        artistIds = []
                        for artist in artistList:
                            artists.append(artist.strip())
                        for artist in artists:
                            artistCheck = Artists.query.filter_by(
                                name=artist).first()
                            if artistCheck == None:
                                newArtist = Artists(name=artist)
                                database.session.add(newArtist)
                        database.session.commit()
                        for artist in artists:
                            artistData = Artists.query.filter_by(
                                name=artist).first()
                            if artist != None:
                                artistIds.append(artistData.id)
                        song.artistId = artistIds[0]
                        song.allArtists = str(artistIds)

                if songMetadata["title"] != None:
                    if songMetadata["title"] != song.name:
                        song.name = songMetadata["title"]

                if songMetadata["album"] != None:
                    if song.albumId == 1:
                        albumName = songMetadata["album"]
                        albumCheck = Albums.query.filter_by(
                            name=albumName).first()
                        if albumCheck == None:
                            album = Albums(
                                name=albumName, artistId=1, genreId=1)
                            database.session.add(album)
                            database.session.commit()
                        albumData = Albums.query.filter_by(
                            name=albumName).first()
                        if albumData != None:
                            song.albumId = int(albumData.id)
                database.session.commit()
            return jsonify(status="OK")

        @api.route('/music/library/ext-update/')
        def externalApiMetadata():
            songList = Songs.query.all()
            data = []
            for song in songList:
                artistNames = ""
                if song.allArtists != None:
                    for artist in json.loads(song.allArtists):
                        artistData = Artists.query.filter_by(id=artist).first()
                        artistNames = artistNames + artistData.name
                data.append({
                    "name": str(song.name),
                    "artists": str(artistNames)
                })

            multiprocessing.log_to_stderr()
            pool = multiprocessing.Pool(processes=16)
            result = pool.map(getMetadata, data)
            return jsonify(status="OK", data=data, result=result)

    def postRoutes(self, api, database):
        pass
