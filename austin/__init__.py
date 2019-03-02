from flask import Flask, render_template, request, flash, redirect, url_for
from passlib.hash import sha256_crypt

from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.sql import func

from austin.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


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

    def __repr__(self):
        return(self.username + ", " + self.email)


def create_app(class_config=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    # Init app contenxts
    db.init_app(app)
    login_manager.init_app(app)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('users/login.html')

        else:
            email = request.form.get('email')
            password_candidate = request.form.get('password')

            # Query for a user with the provided username
            result = User.query.filter_by(email=email).first()

            # If a user exsists and passwords match - login
            if result is not None and sha256_crypt.verify(password_candidate, result.password):

                # Init session vars
                login_user(result)

                flash('Successful Login!', 'success')
                return redirect(url_for('main.index'))

            else:
                flash('Incorrect Login!', 'danger')
                return redirect(url_for('main.index'))

    from austin.endpoints.main.routes import main
    from austin.endpoints.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
