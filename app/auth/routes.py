from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


def _bad_request(msg: str, code: int = 400):
    return jsonify({"error": msg}), code


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return _bad_request("email and password required")
    if len(password) < 8:
        return _bad_request("password must be at least 8 characters")

    if User.query.filter_by(email=email).first():
        return _bad_request("email already registered", 409)

    user = User(email=email, password_hash=pbkdf2_sha256.hash(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not pbkdf2_sha256.verify(password, user.password_hash):
        return _bad_request("invalid credentials", 401)

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200


@auth_bp.post("/logout")
def logout():
    return jsonify({"logged_out": True}), 200
