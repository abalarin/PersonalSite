import os


class Config():

    SECRET_KEY = os.urandom(12)

    # Postgres keys
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + ':' + DB_PASS + '@45.33.79.194:5432/austinbalarin'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  boto3 Keys for Object Storage
    BOTO_KEY = os.environ.get('BOTO_KEY')
    BOTO_SECRET = os.environ.get('BOTO_SECRET')

    # Github OAuth
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
