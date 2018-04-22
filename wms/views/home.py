from flask import Blueprint, render_template, request, session, redirect
import logging

class homeBlueprint:
    def __init__(self, config, database, security):
        self.home = Blueprint("home", __name__)
        self.main(self.home, config, database, security)

    def main(self, home, config, database, security):
        self.configData = config.configData

        @home.route("/")
        def homePage():
            pageConfig = security.pageData(self.configData, database)
            statistics = {}
            statistics["films"] = 0
            statistics["songs"] = database.Songs.query.count()
            statistics["episodes"] = 0
            return render_template("home/home.html", pageName="Home", config=pageConfig, stats=statistics)

        @home.route("/login/", methods=["GET"])
        def loginPage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("home/login.html", pageName="Login", config=pageConfig)

        @home.route("/login/", methods=["POST"])
        def loginAction():
            pageConfig = security.pageData(self.configData, database)
            username = str(request.form["username"])
            password = str(request.form["password"])
            loginResult = security.login(config, username, password, database)
            if loginResult[0] == True:
                session["userID"] = loginResult[1].id
                session["loggedIn"] = True
                return redirect(str(pageConfig["Request"]["rootURL"]), code=302)
            else:
                return render_template("home/accountError.html", pageName="Login Error", config=pageConfig, errors=loginResult[1])

        @home.route("/register/")
        def registerPage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("home/register.html", pageName="Register", config=pageConfig)

        @home.route("/register/", methods=["POST"])
        def registerAction():
            pageConfig = security.pageData(self.configData, database)
            fname = str(request.form["firstName"])
            lname = str(request.form["lastName"])
            username = str(request.form["username"])
            password = str(request.form["password"])
            passwordConfirm = str(request.form["passwordConfirm"])
            email = str(request.form["email"])
            validation = security.accountValidator(username, password, passwordConfirm, email)
            if validation == []:
                user = database.User(username=username, password=security.passHash(config, password), firstName=fname, lastName=lname, email=email)
                database.db.session.add(user)
                database.db.session.commit()
                userData = database.User.query.filter_by(username=username).first()
                session["userID"] = userData.id
                session["loggedIn"] = True
                return redirect(str(pageConfig["Request"]["rootURL"]), code=302)
            else:
                session["loggedIn"] = False
                return render_template("home/accountError.html", pageName="Registration Error", config=pageConfig, errors=validation)

        @home.route("/logout/", methods=['GET'])
        def logoutPage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("home/logout.html", pageName="Logout", config=pageConfig)

        @home.route("/logout/", methods=['POST'])
        def logoutAction():
            pageConfig = security.pageData(self.configData, database)
            session["loggedIn"] = False
            session["userID"] = None
            return redirect(str(pageConfig["Request"]["rootURL"]), code=302)
