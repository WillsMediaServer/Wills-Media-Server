from flask import Blueprint, render_template, request, session, redirect

class tvBlueprint:
    def __init__(self, config, database, security):
        self.tv = Blueprint("tv", __name__, url_prefix='/tv')
        self.main(self.tv, config, database, security)

    def main(self, tv, config, database, security):
        self.configData = config.configData

        @tv.route("/")
        def filmsHome():
            pageConfig = security.pageData(self.configData, database)
            return render_template("tv/tv.html", pageName="TV Shows", config=pageConfig)
