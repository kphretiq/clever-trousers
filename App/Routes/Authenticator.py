# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urljoin
import bcrypt
from flask import request, redirect, url_for, render_template, flash
from flask_login import UserMixin, login_user, logout_user, login_required
from App.Models import *

def authenticator_routes(app, db, login_manager):

    class AuthUser(UserMixin):

        def get(self, username):
            self.user = User.query.filter(username == username).first()
            return self

        def is_active(self):
            return self.user.active
        
        def is_authenticated(self):
            return self.user.authenticated

        def is_anonymous(self):
            return False

        def get_id(self):
            return self.user.username

    def is_safe_url(target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return test_url.scheme in ('http', 'https') and \
                ref_url.netloc == test_url.netloc

    def get_redirect_target():
        for target in [request.values.get('next'), request.referrer]:
            if not target:
                continue
            if is_safe_url(target):
                app.logger.debug("safe url found: %s"%target)
                return target

    def redirect_back(endpoint, **values):
        target = request.form["next"]
        app.logger.debug("target found: %s"%target)
        if not target or not is_safe_url(target):
            target = url_for(endpoint, **values)
        return redirect(target)

    @login_manager.user_loader
    def load_user(user_id):
        auth_user = AuthUser()
        return auth_user.get(user_id)

    @app.route("/login", methods = ["GET", "POST"])
    def login():
        error = None
        next = get_redirect_target()

        if request.method == "POST":
            no_got = "Username or Password incorrect."
            username = request.form["username"].encode("utf-8")
            password = request.form["password"].encode("utf-8")
            user = User.query.filter(username == username).first()
            if user:
                hashed = user.password 
                if bcrypt.checkpw(password, hashed):
                    user.authenticated = True
                    auth_user = AuthUser()
                    login_user(auth_user.get(user.username))
                    return redirect_back("index")
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
