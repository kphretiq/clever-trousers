# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, flash
from App.Models import *

def public_routes(app, db):

    @app.route("/")
    def index():
        return render_template("public/index.html")

