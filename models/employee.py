from extensions import db
from marshmallow import Schema, fields, validate

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)


class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Employee name is required"}
    )

    department = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Department is required"}
    )

    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required"}
    )
