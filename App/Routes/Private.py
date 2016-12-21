# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required
from App.Models import *
from App.Routes import admin_permission, editor_permission, user_permission

def private_routes(app, db, login_manager, principals):

    @app.route("/private")
    @login_required
    @user_permission.require()
    def private():
        return render_template("private/index.html")

