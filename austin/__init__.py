# pylint: disable=E0611, E0401

from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from austin.config import Config

from austin.botoConfig.configer import getConfig
from austin.botoConfig.authBoto import botoClient, botoResource

config = getConfig(Config.APP_ROOT + '/botoConfig/config.ini')
client = botoClient(Config.BOTO_KEY, Config.BOTO_SECRET, config['object_api']['base_url'], config['object_api']['user'])
resource = botoResource(Config.BOTO_KEY, Config.BOTO_SECRET, config['object_api']['base_url'], config['object_api']['user'])

db = SQLAlchemy()
login_manager = LoginManager()

# For some reason gunicorn does not like user_loader outside of this __init__
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    register_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    password = db.Column(db.String(256))
    spotify_code = db.Column(db.String(256))

    def __repr__(self):
        return(self.username + ", " + self.email)


def create_app(class_config=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    # Init app contenxts
    db.init_app(app)
    login_manager.init_app(app)

    from austin.endpoints.main.routes import main
    from austin.endpoints.users.routes import users
    from austin.endpoints.gallery.routes import gallery

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(gallery)

    return app
