from flask import Blueprint, request, jsonify
from models.asset import Asset
from extensions import db
from flask_jwt_extended import jwt_required
from utils.role_required import role_required


asset_bp = Blueprint("asset", __name__)


@asset_bp.route("/assets", methods=["POST"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def create_asset():
    data = request.get_json()
    asset_tag = data.get("asset_tag")
    name = data.get("name")

    if not asset_tag or not name:
        return jsonify(msg="Asset tag and name are required"), 400

    asset = Asset(asset_tag=asset_tag, name=name)

    try:
        db.session.add(asset)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error creating asset: {str(e)}"), 500

    return jsonify(msg="Asset created"), 201



@asset_bp.route("/assign", methods=["POST"])
@jwt_required()
@role_required(["admin", "asset_manager"])
def assign_asset():
    data = request.get_json()
    asset_id = data.get("asset_id")
    employee_id = data.get("employee_id")

    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify(msg="Asset not found"), 404
    if asset.status == "assigned":
        return jsonify(msg="Asset already assigned"), 400

    assignment = AssetAssignment(asset_id=asset.id, employee_id=employee_id)
    asset.status = "assigned"

    try:
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg=f"Error assigning asset: {str(e)}"), 500

    return jsonify(msg="Asset assigned"), 200


