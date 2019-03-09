from sqlalchemy.sql import func
from austin import db

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    spotify_code = db.Column(db.String(256))

    def __repr__(self):
        return(str(self.id) + ", " + self.name)
