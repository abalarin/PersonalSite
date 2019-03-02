from flask import Flask

# from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from sqlalchemy.sql import func

from austin.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     username = db.Column(db.String(120), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     admin = db.Column(db.Boolean, default=False)
#     register_date = db.Column(db.DateTime(
#         timezone=True), server_default=func.now())
#
#     def __repr__(self):
#         return(self.username + ", " + self.email)


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
