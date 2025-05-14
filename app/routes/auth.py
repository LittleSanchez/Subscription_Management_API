from flask import Blueprint, request, jsonify
from app.db import db
from app.models.user import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt
from app.utils.token_blocklist import add_to_blocklist

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    surname = data.get("surname")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(email=email, name=name, surname=surname)
    user.set_password(password)
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
