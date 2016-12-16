# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required
from App.Models import *

def private_routes(app, db, login_manager):

    @app.route("/private")
    @login_required
    def private():
        return render_template("private/index.html")

