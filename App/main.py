# -*- coding: utf-8 -*-
import click
from flask import Flask, session
from flask_session import Session
from flask_cache import Cache
from flask_login.login_manager import LoginManager
from flaskext.markdown import Markdown
from App.Async.CeleryAsync import celery_async

from App.Models import db
from App.Models import User

from App.Routes.Authenticator import authenticator_routes
from App.Routes.Public import public_routes
from App.Routes.Private import private_routes

app = Flask(__name__)
app.config.from_object("config")
# must have secret key to use authentication of any sort
app.secret_key = app.config["APP_SECRET_KEY"]
# add rotating file handler created in config
app.logger.addHandler(app.config["RFH"])

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#login_manager.login_message = u"Why here and not the accursed initial login?"

#celery = celery_async(app)
cache = Cache()

# set session type as environment variable
Session(app)

# add markdown filter
Markdown(app, extensions=["nl2br", "fenced_code", "tables",])

authenticator_routes(app, db, login_manager)
private_routes(app, db, login_manager)
public_routes(app, db)

#### Command line bits
# TODO get values from environment
@app.cli.command()
@click.option("--username", default=None, help="root username")
@click.option("--password", default=None, help="root password")
@click.option("--email", default=None, help="root email")
def init_root(username, email, password):
    import sys
    import getpass
    from App.Routes.Authenticator import user_add

    initialized = False
    try:
        User.query.one()
        click.echo("root user already created. you'd best skeedaddle.")
        initialized = True
    except:
        pass

    if initialized:
        sys.exit(1)

    db.create_all()
    click.echo("initialized database")
    status, message = user_add(db, username, password, email, role="root")
    sys.exit(str(message))
