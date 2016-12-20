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

# If we don't have a root user, add initializer routes
# This prevents initializer routes from being initialized after database and
# root user have been created.
# After app is restarted, the Routes.Initializer
#with app.app_context():
#    try:
#        User.query.one()
#    except Exception as error:
#        app.logger.warning("Create a root user, then restart app!")
#        from App.Routes.Initializer import initializer_routes
#        initializer_routes(app, db)

@app.cli.command()
@click.option("--username", default=None, help="root username")
@click.option("--email", default=None, help="root email")
def init_root(username, email):
    #TODO re-use user auth
    import sys
    import getpass
    import bcrypt
    import uuid

    initialized = False
    try:
        User.query.one()
        click.echo("root user already created. you'd best skeedaddle.")
        initialized = True
    except:
        pass

    if initialized:
        sys.exit(1)

    password = getpass.getpass("Enter password for %s: "%username).encode("utf-8")
    password_redux = getpass.getpass("Repeat: ").encode("utf-8")
    if not password == password_redux:
        sys.exit("password mismatch")

    api_key = str(uuid.uuid4()).encode("utf-8")
    session_token = str(uuid.uuid4()).encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    api_key_hashed = bcrypt.hashpw(api_key, bcrypt.gensalt())

    db.create_all()
    click.echo("initialized database")

    user = User(
            username = username,
            password = hashed,
            email = email,
            session_token = session_token,
            api_key = api_key_hashed,
            active = True,
            authenticated = True,
            )
    db.session.add(user)
    db.session.commit()
    click.echo("api_key: %s "%api_key)
    sys.exit(0)

