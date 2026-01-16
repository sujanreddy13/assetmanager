from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.asset import Asset, AssetSchema
from models.assignment import AssetAssignment, AssetAssignmentSchema
from utils.role_required import role_required

filter_bp = Blueprint("filter_bp", __name__)


# @filter_bp.route("/assets", methods=["GET"])
# @jwt_required()
# @role_required(["admin", "asset_manager", "employee"])
# def list_assets():
#     asset = Asset.query.all()
#     schema = AssetSchema(many=True)
#     return jsonify(schema.dump(asset)), 200
@filter_bp.route("/assets", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def list_assets():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = Asset.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    assets = pagination.items
    schema = AssetSchema(many=True)

    return jsonify({
        "total_records": pagination.total,
        "total_pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "assets": schema.dump(assets)
    }), 200


@filter_bp.route("/assets/<int:asset_id>", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify(msg="Asset not found"), 404
    
    schema = AssetSchema()
    return jsonify(schema.dump(asset)), 200


@filter_bp.route("/assignments/<int:asset_id>", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_asset_assignment(asset_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = (
        AssetAssignment.query
        .filter_by(asset_id=asset_id)
        .order_by(AssetAssignment.assigned_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    if pagination.total == 0:
        return jsonify(msg="No assignments found for this asset"), 404

    schema = AssetAssignmentSchema(many=True)

    return jsonify({
        "total_records": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "assignments": schema.dump(pagination.items)
    }), 200


    # result = []
    # for a in assignments:
    #     result.append({
    #         "asset_id": a.asset_id,
    #         "employee_id": a.employee_id,
    #         "assigned_at": a.assigned_at,
    #         "released_at": a.released_at
    #     })

    # return jsonify(result), 200


@filter_bp.route("/release", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_release_history():
    page=request.args.get("page", 1, type=int)
    per_page=request.args.get("per_page", 5, type=int)

    pagination = (
        AssetAssignment.query.filter_by(released_at=None)
        .order_by(AssetAssignment.assigned_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    if pagination.total == 0:
        return jsonify(msg="No active assignments found"), 404

    schema = AssetAssignmentSchema(many=True)
    return jsonify({
        "total_records": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "assignments": schema.dump(pagination.items)
    }), 200

    

@filter_bp.route("/release/<int:asset_id>", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_asset_release_history(asset_id):
    page=request.args.get("page", 1, type=int)
    per_page=request.args.get("per_page", 5, type=int)

    pagination = (
        AssetAssignment.query.filter(AssetAssignment.asset_id==asset_id, AssetAssignment.released_at.isnot(None))
        .order_by(AssetAssignment.released_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    if pagination.total == 0:
        return jsonify(msg="No release history found for this asset"), 404

    schema = AssetAssignmentSchema(many=True)
    return jsonify({
        "total_records": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "assignments": schema.dump(pagination.items)
    }), 200

    # result = []
    # for a in assignments:
    #     result.append({
    #         "asset_id": a.asset_id,
    #         "employee_id": a.employee_id,
    #         "assigned_at": a.assigned_at,
    #         "released_at": a.released_at
    #     })

    # return jsonify(result), 200



@filter_bp.route("/retired", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_retired_assets():
    page=request.args.get("page", 1, type=int)
    per_page=request.args.get("per_page", 5, type=int)

    pagination = (
        Asset.query.filter_by(status="retired")
        .order_by(Asset.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    if pagination.total == 0:
        return jsonify(msg="No retired assets found"), 404

    schema = AssetSchema(many=True)
    return jsonify({
        "total_records": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "assets": schema.dump(pagination.items)
    }), 200


@filter_bp.route("/retired/<int:asset_id>", methods=["GET"])
@jwt_required()
@role_required(["admin", "asset_manager", "employee"])
def get_retired_asset(asset_id):
    asset = Asset.query.filter_by(id=asset_id, status="retired").first()
    if not asset:
        return jsonify(msg="Retired asset not found"), 404

    schema = AssetSchema()
    return jsonify(schema.dump(asset)), 200