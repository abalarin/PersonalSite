import os


class Config():

    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SECRET_KEY = os.urandom(12)

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + ':' + DB_PASS + '@45.33.79.194:5432/austinbalarin'

    # Connection to local postgres db
    # SQLALCHEMY_DATABASE_URI = 'postgresql://abalarin:lindoe!@localhost:5432/austinbalarin'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
