from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# rigister route for new users

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return jsonify(msg="User already exists"), 400

    # Hash the password and sac=ving it in the db
    hashed_password = generate_password_hash(data["password"])
    user = User(
        email=data["email"],
        password=hashed_password,
        role=data.get("role", "user")  
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(msg="User registered successfully"), 201



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify(msg="Invalid credentials"), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify(token=token)
