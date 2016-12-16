import os
import platform
import logging, logging.handlers

BASEDIR = os.path.abspath(os.path.dirname(__file__))

########### Logging ########### 
# create a nice rotating file handler for logging.
# added to app logger in 
logpath = os.path.join(BASEDIR, "logs")
if not os.path.exists(logpath):
    os.mkdir(logpath)
logfile = os.path.join(logpath, "fact-chucker.log")
format_string = "%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s"
formatter = logging.Formatter(format_string)
RFH = logging.handlers.RotatingFileHandler(
        logfile,
        maxBytes=10000000,
        backupCount=5)
RFH.setLevel(logging.DEBUG)
RFH.setFormatter(formatter)

########### Flask ########### 
# required if you wish to use any sort of Authentication
APP_SECRET_KEY = "7481bfe8-9b03-41c3-b514-5d14b961683b"
# used by App.Admin for creating initial database. If DB already exists, running
# the init script again does nothing, so this is kind of "meh".
ADMIN_SECRET_KEY = "1aed2cb9-261f-4088-81dd-3d577d292c67"

# Display debug information in console
DEBUG = True
# Display debug information in browser
TEMPLATE_DEBUG = DEBUG

########### Cache ########### 
# flask-auth / flask-session requires redis for our purposes
# figure out how to point to socket
SESSION_TYPE = "redis"
# flask-cache needs to know about redis as well 
CACHE_TYPE = "redis"

########### Database ########### 

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"
SQLALCHEMY_DATABASE_NAME = "fact"
SQLALCHEMY_TRACK_MODIFICATIONS = False

########### Celery ########### 
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_BACKEND = CELERY_BROKER_URL

# clean up unneeded modules
del os
del platform
