from flask import Blueprint, request, jsonify
from models.employee import Employee
from extensions import db
from flask_jwt_extended import jwt_required

employee_bp = Blueprint("employee", __name__)
@employee_bp.route("/employees", methods=["POST"])
@jwt_required()
def create_employee():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    department = data.get("department")

    if not name or not email:
        return jsonify(msg="Name and email are required"), 400

    emp = Employee(
        name=name,
        email=email,
        department=department
    )

    db.session.add(emp)
    db.session.commit()
    return jsonify(msg="Employee created"), 201
