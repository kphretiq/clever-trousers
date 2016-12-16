# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urljoin
from flask import request, redirect
from flask_login import UserMixin
from App.Models import User

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
            return target

def redirect_back(endpoint, **values):
    target = request.form["next"]
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

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
        return self.user.session_token
