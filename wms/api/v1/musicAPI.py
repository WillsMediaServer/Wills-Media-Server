#
# /wms/api/v1/musicAPI.py
# Wills Media Server Core
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

from flask import jsonify, request
import logging

class Music:
    def __init__(self, api, database):
        self.logger = logging.getLogger('wms.api')
        self.logger.debug("Adding Music API Endpoints")
        self.routes(api, database)

    def routes(self, api, database):
        
        @api.route('/music/songs/', methods=['GET'])
        def songs():
            return "OK"

        @api.route('/music/songs/<int:id>', methods=['GET'])
        def songId(id):
            return jsonify(id=str(id), status="OK")

        @api.route('/music/artists/', methods=['GET'])
        def artists():
            return "OK"

        @api.route('/music/artists/<int:id>', methods=['GET'])
        def artistId(id):
            return jsonify(id=str(id), status="OK")

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
