from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
)

from app.db import db
from app.models.user import User
from app.utils.token_blocklist import add_to_blocklist
from app.utils.validators import PasswordValidationError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required_fields = ["email", "password", "name", "surname"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    email = data["email"].strip().lower()
    name = data["name"].strip()
    surname = data["surname"].strip()
    password = data["password"]

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(email=email, name=name, surname=surname)

    try:
        user.set_password(password)
    except PasswordValidationError as e:
        return jsonify({"message": str(e)}), 400

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return (
        jsonify(
            {
                "access_token": access_token,
                "user": {
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname,
                },
            }
        ),
        200,
    )


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    add_to_blocklist(jti)
    return jsonify({"message": "Logged out successfully"}), 200
