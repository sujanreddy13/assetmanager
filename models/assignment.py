from extensions import db
from datetime import datetime

class AssetAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    released_at = db.Column(db.DateTime)
