from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.asset import Asset, AssetSchema
from models.assignment import AssetAssignment
from models.employee import Employee
from extensions import db
from flask_jwt_extended import jwt_required
from utils.role_required import role_required
from datetime import datetime

asset_bp = Blueprint("asset", __name__)

# @asset_bp.route("/assets", methods=["POST"])
# @jwt_required()
# @role_required(["admin", "asset_manager"])
# def create_asset():
#     data = request.get_json()
#     asset_tag = data.get("asset_tag")
#     name = data.get("name")

#     if not asset_tag or not name:
#         return jsonify(msg="Asset tag and name are required"), 400

#     asset = Asset(asset_tag=asset_tag, name=name)

#     try:
#         db.session.add(asset)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify(msg=f"Error creating asset: {str(e)}"), 500

#     return jsonify(msg="Asset created"), 201
@asset_bp.route("/assets", methods=["POST"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def create_asset():
    schema = AssetSchema()

    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(errors=err.messages), 400

    asset = Asset(
        asset_tag=data["asset_tag"],
        name=data["name"]
    )

    try:
        db.session.add(asset)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg="Error creating asset"), 500

    return jsonify(msg="Asset created successfully"), 201



@asset_bp.route("/assign", methods=["POST"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def assign_asset():
    data = request.get_json()
    asset_id = data.get("asset_id")
    employee_id = data.get("employee_id")

    asset = Asset.query.get(asset_id)
    employee = Employee.query.get(employee_id)
    if not asset:
        return jsonify(msg="Asset not found"), 404
    if not employee:
        return jsonify(msg="Employee not found"), 404
    if asset.status == "assigned":
        return jsonify(msg="Asset already assigned"), 400
    if asset.status == "retired":
        return jsonify(msg="Cannot assign a retired asset"), 400


    assignment = AssetAssignment(asset_id=asset.id, employee_id=employee.id)
    asset.status = "assigned"

    try:
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error assigning asset: {str(e)}"), 500

    return jsonify(msg="Asset assigned"), 200





@asset_bp.route("/release/<int:asset_id>", methods=["PUT"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def release_asset(asset_id):
    assignment = AssetAssignment.query.filter_by(asset_id=asset_id, released_at=None).first()
    if not assignment:
        return jsonify(msg="No active assignment found"), 404

    assignment.released_at = datetime.utcnow()
    assignment.asset = Asset.query.get(asset_id) 
    assignment.asset.status = "available"

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error releasing asset: {str(e)}"), 500

    return jsonify(msg="Asset released"), 200


@asset_bp.route("/retire/<int:asset_id>", methods=["PUT"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def retire_asset(asset_id):
    asset = Asset.query.get(asset_id)

    if not asset:
        return jsonify(msg="Asset not found"), 404

    if asset.status == "assigned":
        return jsonify(msg="Cannot retire an assigned asset"), 400

    if asset.status == "retired":
        return jsonify(msg="Asset already retired"), 400

    asset.status = "retired"
    asset.retired_at = datetime.utcnow()

    db.session.commit()

    return jsonify(msg="Asset retired successfully"), 200

#filtering 



    


@asset_bp.route("/assignments", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def assignment_history():
    assignments = AssetAssignment.query.all()
    result = []

    for a in assignments:
        result.append({
            "asset_id": a.asset_id,
            "employee_id": a.employee_id,
            "assigned_at": a.assigned_at,
            "released_at": a.released_at
        })

    return jsonify(result), 200


