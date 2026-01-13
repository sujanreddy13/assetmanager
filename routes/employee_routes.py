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

@employee_bp.route("/employees", methods=["GET"])
@jwt_required()
def list_employees():
    employees = Employee.query.all()
    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
            "created_at": emp.created_at
        })

    return jsonify(result), 200


@employee_bp.route("/employees/<int:employee_id>", methods=["GET"])
@jwt_required()
def get_employee(employee_id):
    emp = Employee.query.get(employee_id)
    if not emp:
        return jsonify(msg="Employee not found"), 404

    result = {
        "id": emp.id,
        "name": emp.name,
        "email": emp.email,
        "department": emp.department,
        "created_at": emp.created_at
    }

    return jsonify(result), 200
