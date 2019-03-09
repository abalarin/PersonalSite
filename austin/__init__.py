from flask import Flask, session
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

    @app.before_request
    def visits():
        if 'visit_count' in session:
            session['visit_count'] = session.get('visit_count') + 1
        else:
            session['visit_count'] = 1

        print(session['visit_count'])

    # Init app contenxts
    db.init_app(app)

    # Init Logi Manager
    from austin.models.user_models import load_user
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    from austin.endpoints.main.routes import main
    from austin.endpoints.users.routes import users
    from austin.endpoints.gallery.routes import gallery

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(gallery)

    return app
