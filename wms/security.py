from flask import session, request, render_template
import logging, re

class Security:
    def __init__(self, config):
        logging.info("Initialising Security")

    def accountValidator(self, username, password, passwordConfirm, email):
        error = []
        if len(username) < 5:
            error.append("Username is too short!")
        if len(username) > 250:
            error.append("Username is too long!")
        if len(password) < 8:
            error.append("Password is too short!")
        if len(password) > 60:
            error.append("Password is too long!")
        if password != passwordConfirm:
            error.append("Passwords Don't Match!")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error.append("Email is not valid")

        return error

def login(username, password, database):
    errors = []
    # check for empty fields
    if username == "" or username == None:
        errors.append("username is Empty")
    if password == "" or password == None:
        errors.append("password is Empty")

    # get userData for the requested Username
    userData = database.User.query.filter_by(username=username).first()
    if userData == None:
        errors.append("User doesn't Exist")
    else:
        if userData.password != password:
            errors.append("Incorrect password")

    # returns the userdata if there are no errors
    if errors == []:
        return [True, userData]
    else:
        return [False, errors]

def pageData(pageData, database):
    pageData["User"] = {}
    if session.get("loggedIn") == False:
        pageData["User"]["loggedIn"] = False
    else:
        if session.get("userID") != None:
            userData = database.User.query.get(session.get("userID"))
            pageData["User"]["loggedIn"] = True
            pageData["User"]["firstName"] = userData.firstName
            pageData["User"]["lastName"] = userData.lastName
            pageData["User"]["fullName"] = userData.fullName
            pageData["User"]["username"] = userData.username
            pageData["User"]["email"] = userData.email
    pageData["Request"] = {}
    pageData["Request"]["rootURL"] = str(request.url_root)
    return pageData
