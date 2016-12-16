# -*- coding: utf-8 -*-
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

        """

        error = None

        # Big fails first
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

                password = request.form["password"].encode("utf-8")
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password, salt)

                user = User(
                        username = request.form["username"].encode("utf-8"),
                        password = hashed,
                        email = "private@dont.bug.me",
                        role = "root",
                        active = True,
                        )
                db.session.add(user)
                db.session.commit()
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
