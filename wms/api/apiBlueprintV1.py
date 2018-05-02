#
# /wms/api/apiBlueprintV1.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

from flask import Blueprint, request, jsonify
import logging

class api:
    def __init__(self, database):
        self.logger = logging.getLogger(__name__)
        self.api = Blueprint("apiV1", __name__, url_prefix='/api/v1')
        self.main(self.api, database)

    def main(self, api, database):

        @api.errorhandler(404)
        def apiError404(err):
            return jsonify(error="Error 404 Not Found")

        @api.errorhandler(500)
        def apiError500(err):
            self.logger.error("Error 500: {}".format(err))
            return jsonify(error="Error 404 Server Issue")

        @api.route('/music/', methods=['GET'])
        def apiMusicRoot():
            return "OK"

        @api.route('/music/songs/', methods=['GET'])
        def apiMusicSongs():
            return "OK"

        @api.route('/music/artists/', methods=['GET'])
        def apiMusicArtists():
            return "OK"

        @api.route('/music/albums/', methods=['GET'])
        def apiMusicAlbums():
            return "OK"
