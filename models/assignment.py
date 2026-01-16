from extensions import db
from marshmallow import Schema, fields, validate
from datetime import datetime

class AssetAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    released_at = db.Column(db.DateTime)


class AssetAssignmentSchema(Schema):
    id = fields.Int(dump_only=True)

    asset_id = fields.Int(
        required=True,
        error_messages={"required": "Asset ID is required"}
    )

    employee_id = fields.Int(
        required=True,
        error_messages={"required": "Employee ID is required"}
    )

    assigned_at = fields.DateTime(dump_only=True)
    released_at = fields.DateTime(dump_only=True, allow_none=True)

