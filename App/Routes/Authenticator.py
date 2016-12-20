# -*- coding: utf-8 -*-
import uuid
import bcrypt
from flask import request, redirect, url_for, render_template, flash
from flask_login import  login_user, logout_user, login_required
from App.Models import User
from App.Routes.AuthCommon import *

def user_add(db, username, password, email, role="user"):

    session_token = str(uuid.uuid4()).encode("utf-8")
    api_key = str(uuid.uuid4()).encode("utf-8")

    username = username.encode("utf-8")
    password = password.encode("utf-8")
    email = email.encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    user = User(
            username = username,
            password = hashed,
            email = email,
            active = True,
            session_token = session_token,
            api_key = api_key,
            )
    try:
        db.session.add(user)
        db.session.commit()
        return True, "User created"
    except Exception as error:
        return False, error

def authenticator_routes(app, db, login_manager):

    @login_manager.user_loader
    def load_user(session_token):
        auth_user = AuthUser()
        return auth_user.get(session_token)

    @app.route("/login", methods = ["GET", "POST"])
    def login():
        error = None
        next = get_redirect_target()

        if request.method == "POST":
            username = request.form["username"].encode("utf-8")
            password = request.form["password"].encode("utf-8")
            user = User.query.filter(username == username).first()
            if user:
                hashed = user.password 
                if bcrypt.checkpw(password, hashed):
                    user.authenticated = True
                    auth_user = AuthUser()
                    login_user(auth_user.get(user.session_token))
                    return redirect_back("index")

            flash("Username or Password incorrect.")
        return render_template(
                "authenticate/login.html",
                next=next,
                error=error,
                )
    
    @app.route("/logout", methods = ["GET", "POST"])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/signup", methods = ["GET", "POST"])
    def signup():
        # TODO send confirmation email
        if request.method == "POST":
            fail = False

            if not request.form["username"]:
                fail = True
                flash("Username required")

            if not request.form["password"] == request.form["repeat-password"]:
                fail = True
                flash("Passphrases do not match.")

            if not request.form["email"] == request.form["repeat-email"]:
                fail = True
                flash("Email addresses do not match.")

            if not fail:
                username = request.form["username"]
                password = request.form["password"]
                email = request.form["email"]
                status, message = user_add(db, username, password, email)
                flash(message)
                if status:
                    return redirect(url_for("login"))

        return render_template("authenticate/signup.html")

#TODO change password, change session_token
