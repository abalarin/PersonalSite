from sqlalchemy.sql import func
from austin import db


class User(db.Model):
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
