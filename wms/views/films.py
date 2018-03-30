from flask import Blueprint, render_template, request, session, redirect

class filmsBlueprint:
    def __init__(self, config, database, security):
        self.films = Blueprint("films", __name__, url_prefix='/films')
        self.main(self.films, config, database, security)

    def main(self, films, config, database, security):
        self.configData = config.configData

        @films.route("/")
        def filmsHome():
            pageConfig = security.pageData(self.configData, database)
            return render_template("films/films.html", pageName="Films", config=pageConfig)
