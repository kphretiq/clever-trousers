# -*- coding: utf-8 -*-
from flask import request
from flask.ext import restful
from flask_restful import reqparse
from flask_login import login_user, login_required
from App.Models import User
from App.Routes.AuthCommon import *

def test_api(app, db, login_manager):

    @login_manager.request_loader
    def load_user_from_request(request):
        api_key = request.args.get("api_key").encode("utf-8")
        api_secret = request.args.get("api_secret").encode("utf-8")
        if api_key:
            user = User.query.filter(api_key == api_key).first()
            if bcrypt.checkpw(api_secret, user.api_secret):
                if user:
                    return user
        return None
