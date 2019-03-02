from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from austin.config import Config

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

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
