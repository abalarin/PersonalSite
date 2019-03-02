from sqlalchemy.sql import func
from flask_login import UserMixin
from austin import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


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
