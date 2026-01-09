from extensions import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(20), default="available")
