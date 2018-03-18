from flask import Blueprint, render_template, request, session, redirect

class musicBlueprint:
    def __init__(self, config, database, security):
        self.music = Blueprint("music", __name__, url_prefix='/music')
        self.main(self.music, config, database, security)

    def main(self, music, config, database, security):
        self.configData = config.configData

        @music.route("/")
        def musicHomePage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("music/music.html", pageName="Music", config=pageConfig)
