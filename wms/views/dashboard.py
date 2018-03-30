from flask import Blueprint, render_template, request, session, redirect

class dashboardBlueprint:
    def __init__(self, config, database, security):
        self.dashboard = Blueprint("dashboard", __name__, url_prefix='/dashboard')
        self.main(self.dashboard, config, database, security)

    def main(self, dashboard, config, database, security):
        self.configData = config.configData

        @dashboard.route("/")
        def dashboardPage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("dashboard/dashboard.html", pageName="Dashboard", config=pageConfig)

        @dashboard.route("/settings/")
        def settingsHomePage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("dashboard/settings.html", pageName="Settings", config=pageConfig)

        @dashboard.route("/statistics/")
        def statisticsPage():
            pageConfig = security.pageData(self.configData, database)
            return render_template("dashboard/statistics.html", pageName="Statistics", config=pageConfig)

        @dashboard.route("/profile/")
        def userProfilePage():
            pageConfig = security.pageData(self.configData, database)
            if pageConfig["User"]["loggedIn"] == False:
                pageConfig["User"]["username"] = ""
            return render_template("dashboard/profile.html", pageName="Your Profile", config=pageConfig, user=pageConfig["User"]["username"])

        @dashboard.route("/profile/<username>")
        def profilePage(username):
            pageConfig = security.pageData(self.configData, database)
            return render_template("dashboard/profile.html", pageName=username+"'s Profile'", config=pageConfig, user=username)
