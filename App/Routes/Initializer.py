# -*- coding: utf-8 -*-
import uuid
import bcrypt
from flask import request, render_template, flash
from App.Models import *

def initializer_routes(app, db):

    @app.route("/init/<string:admin_secret_key>", methods = ["GET", "POST"])
    def initialize(admin_secret_key):
        """
        check for root user (1): fail if exists
        check for secret key: fail if mismatch
        set default role = "root"
        set default email address
        create api_key
        create user_token
        """

        error = None
        try:
            User.query.one()
            flash("BEGONE!")
            error = "Admin already exists!"
            return render_template("error.html", error=error)
        except:
            pass

        if not admin_secret_key == app.config["ADMIN_SECRET_KEY"]:
            error = "Key Mismatch"
            return render_template("error.html", error=error)

        if request.method == "POST":

            if not request.form["password"] == request.form["repeat-password"]:
                flash("Try again.")
                return render_template("initializer/index.html",
                        error="Passphrases do not match!")

            if not request.form["username"]:
                flash("Username required.")
                return render_template("initializer/index.html",
                        error="Not even a single letter? Sheesh.")

            try:
                api_key = str(uuid.uuid4()).encode("utf-8")
                api_secret = str(uuid.uuid4()).encode("utf-8")

                session_token = str(uuid.uuid4()).encode("utf-8")
                password = request.form["password"].encode("utf-8")
                hashed = bcrypt.hashpw(password, bcrypt.gensalt()) 
                user = User(
                        username = request.form["username"].encode("utf-8"),
                        password = hashed,
                        email = "private@dont.bug.me",
                        role = "root",
                        active = True,
                        session_token = session_token,
                        api_key = api_key,
                        )

                db.session.add(user)
                db.session.commit()
                flash("keep track of these keys!")
                flash("api_key: %s"%api_key)
                flash("api_secret: %s"%api_secret)
                return render_template("error.html", error = "Root user created. Restart app!")

            except Exception as db_error:
                error = db_error
                flash("Username Error")

        if not error:
            try:
                db.create_all()
                flash("Initialized Database")
            except Exception as error:
                flash("Database Creation Error!")

        return render_template("initializer/index.html", error=error)
