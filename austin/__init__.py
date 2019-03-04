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
