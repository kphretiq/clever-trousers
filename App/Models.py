# -*- coding: utf-8 -*-
import datetime
from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(36), unique=True, nullable=False)
    username = db.Column(db.String(72), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    api_key = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated = db.Column(db.DateTime, default=datetime.datetime.utcnow(),
            onupdate=datetime.datetime.utcnow())
