import os

import json
import urllib3

with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json') as config_file:
    config = json.load(config_file)

class Config():

    SECRET_KEY = os.urandom(12)

    # Postgres keys
    DB_USER = config.get('DB_USER')
    DB_PASS = config.get('DB_PASS')

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + ':' + DB_PASS + '@45.33.79.194:5432/austinbalarin'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  boto3 Keys for Object Storage
    BOTO_KEY = config.get('BOTO_KEY')
    BOTO_SECRET = config.get('BOTO_SECRET')

    # Github OAuth
    GITHUB_TOKEN = config.get('GITHUB_TOKEN')

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    # Spotify Stuff
    SPOTIFY_REDIRECT = config.get('SPOTIFY_REDIRECT')
    SPOTIFY_ID = config.get('SPOTIFY_ID')
    SPOTIFY_SECRET = config.get('SPOTIFY_SECRET')
