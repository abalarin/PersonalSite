from austin import db


class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    spotify_code = db.Column(db.String(256))
    spotify_access_token = db.Column(db.String(256))
    spotify_refresh_token = db.Column(db.String(256))
    snap_client_id = db.Column(db.String(256))

    def __repr__(self):
        return(str(self.id) + ", " + self.name)
