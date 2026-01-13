from extensions import db
from marshmallow import Schema, fields, validate

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(20), default="available")

    retired_at = db.Column(db.DateTime, nullable=True)


class AssetSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    retired_at = fields.DateTime(dump_only=True)

    asset_tag = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Asset tag is required"}
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Asset name is required"}
    )
