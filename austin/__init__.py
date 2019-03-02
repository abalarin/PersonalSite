from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from austin.config import Config

db = SQLAlchemy()


def create_app(class_config=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from austin.endpoints.main.routes import main
    from austin.endpoints.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
