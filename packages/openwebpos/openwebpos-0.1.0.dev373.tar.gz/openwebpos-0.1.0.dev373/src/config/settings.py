import os
from datetime import timedelta
from os import getenv

# Application Settings
APP_PATH = getenv('APP_PATH', os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
APP_ENV_PATH = getenv('APP_ENV_PATH', APP_PATH)
APP_RESTARTED = getenv('APP_RESTARTED', False)
DB_CONFIGURED = getenv('DB_CONFIGURED', False)
DB_DATA_INSERTED = getenv('DB_DATA_INSERTED', False)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = getenv('UPLOAD_FOLDER', os.path.join(APP_PATH, 'uploads'))

# Flask Config
DEBUG = getenv('DEBUG', False)
TESTING = getenv('TESTING', False)
SECRET_KEY = getenv('SECRET_KEY', 'dev-key')
SERVER_NAME = getenv('SERVER_NAME', 'localhost:5000')
PREFERRED_URL_SCHEME = getenv('PREFERRED_URL_SCHEME', 'https')

# Flask-Login
# https://flask-login.readthedocs.io/en/latest/
# timedelta(7) = 7 days
REMEMBER_COOKIE_DURATION = timedelta(7)
SESSION_PROTECTION = 'strong'

# Flask-SQLAlchemy
# DB_DIALECT = getenv('DB_DIALECT')
# DB_DRIVER = getenv('DB_DRIVER', None)
# DB_USER = getenv('DB_USER')
# DB_PASS = getenv('DB_PASS')
# DB_HOST = getenv('DB_HOST')
# DB_PORT = getenv('DB_PORT', None)
# DB_NAME = getenv('DB_NAME')

if DB_CONFIGURED:
    db_uri = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_POOL_RECYCLE = 299
    # SQLALCHEMY_POOL_TIMEOUT = 20
