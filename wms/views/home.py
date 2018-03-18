from flask import Blueprint, render_template, request, session, redirect
import logging
from wms.security import pageData, login

class homeBlueprint:
    def __init__(self, config, database, security):
        self.home = Blueprint("home", __name__)
        self.main(self.home, config, database, security)

    def main(self, home, config, database, security):
        self.configData = config.configData

        @home.route("/")
        def homePage():
            pageConfig = pageData(self.configData, database)
            return render_template("home/home.html", pageName="Home", config=pageConfig)

        @home.route("/login/", methods=["GET"])
        def loginPage():
            pageConfig = pageData(self.configData, database)
            return render_template("home/login.html", pageName="Login", config=pageConfig)

        @home.route("/login/", methods=["POST"])
        def loginAction():
            pageConfig = pageData(self.configData, database)
            username = str(request.form["username"])
            password = str(request.form["password"])
            loginResult = login(username, password, database)
            if loginResult[0] == True:
                session["userID"] = loginResult[1].id
                session["loggedIn"] = True
                return redirect(str(pageConfig["Request"]["rootURL"]), code=302)
            else:
                return render_template("home/accountError.html", pageName="Login Error", config=pageConfig, errors=loginResult[1])

        @home.route("/register/")
        def registerPage():
            pageConfig = pageData(self.configData, database)
            return render_template("home/register.html", pageName="Register", config=pageConfig)

        @home.route("/register/", methods=["POST"])
        def registerAction():
            pageConfig = pageData(self.configData, database)
            fname = str(request.form["firstName"])
            lname = str(request.form["lastName"])
            username = str(request.form["username"])
            password = str(request.form["password"])
            passwordConfirm = str(request.form["passwordConfirm"])
            email = str(request.form["email"])
            validation = security.accountValidator(username, password, passwordConfirm, email)
            if validation == []:
                user = database.User(username=username, password=password, firstName=fname, lastName=lname, email=email)
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
            pageConfig = pageData(self.configData, database)
            return render_template("home/logout.html", pageName="Logout", config=pageConfig)

        @home.route("/logout/", methods=['POST'])
        def logoutAction():
            pageConfig = pageData(self.configData, database)
            session["loggedIn"] = False
            session["userID"] = None
            return redirect(str(pageConfig["Request"]["rootURL"]), code=302)
