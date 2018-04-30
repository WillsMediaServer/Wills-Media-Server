from flask import Blueprint, request, jsonify
import logging

class api:
    def __init__(self, database):
        self.api = Blueprint("home", __name__, url_prefix='/api/v1')
        self.main(self.api, database)

    def main(self, api, database):
        @api.route('/')
        def apiRoot():
            return jsonify({"data":None})

        @api.route('/users/')
        def apiUsersRoot():
            return jsonify({"data":"users"})
