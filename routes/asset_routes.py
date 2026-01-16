from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.asset import Asset, AssetSchema
from models.assignment import AssetAssignment, AssetAssignmentSchema
from models.employee import Employee
from extensions import db
from flask_jwt_extended import jwt_required
from utils.role_required import role_required
from datetime import datetime

asset_bp = Blueprint("asset", __name__)


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

    schema = AssetAssignmentSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    asset = Asset.query.get(data["asset_id"])
    employee = Employee.query.get(data["employee_id"])

    if not asset:
        return jsonify(msg="Asset not found"), 404
    if not employee:
        return jsonify(msg="Employee not found"), 404

    if asset.status == "assigned":
        return jsonify(msg="Asset already assigned"), 400
    if asset.status == "retired":
        return jsonify(msg="Cannot assign a retired asset"), 400

    assignment = AssetAssignment(
        asset_id=asset.id,
        employee_id=employee.id,
        assigned_at=datetime.utcnow()
    )

    asset.status = "assigned"

    try:
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error assigning asset: {str(e)}"), 500

    return jsonify(
        msg="Asset assigned successfully",
        assignment=schema.dump(assignment)
    ), 201


@asset_bp.route("/release/<int:asset_id>", methods=["PUT"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def release_asset(asset_id):

    assignment = AssetAssignment.query.filter_by(asset_id=asset_id, released_at=None).first()

    if not assignment:
        return jsonify(msg="No active assignment found"), 404

    assignment.released_at = datetime.utcnow()
    assignment.asset=Asset.query.get(asset_id)
    assignment.asset.status = "available"

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error releasing asset: {str(e)}"), 500

    schema = AssetAssignmentSchema()
    return jsonify(
        message="Asset released successfully",
        assignment=schema.dump(assignment)), 200



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

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error retiring asset: {str(e)}"), 500
    
    schema = AssetSchema()
    return jsonify(msg="Asset retired successfully", asset=schema.dump(asset)), 200



@asset_bp.route("/assignments", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def assignment_history():
    assignments = AssetAssignment.query.all()
    schema= AssetAssignmentSchema(many=True)
    return jsonify(schema.dump(assignments)), 200
    # result = []

    # for a in assignments:
    #     result.append({
    #         "asset_id": a.asset_id,
    #         "employee_id": a.employee_id,
    #         "assigned_at": a.assigned_at,
    #         "released_at": a.released_at
    #     })

    # return jsonify(result), 200


