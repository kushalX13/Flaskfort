from flask import Blueprint, current_app, jsonify, request
from passlib.hash import pbkdf2_sha256

from app.extensions import db
from app.models import Note, User

dev_bp = Blueprint("dev", __name__)


@dev_bp.get("/dev/db")
def db_snapshot():
    if current_app.config.get("ENV", "production") == "production":
        return jsonify({"error": "not found"}), 404

    users = [
        {"id": u.id, "email": u.email, "created_at": u.created_at}
        for u in User.query.order_by(User.id.asc()).all()
    ]
    notes = [
        {
            "id": n.id,
            "user_id": n.user_id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at,
            "updated_at": n.updated_at,
        }
        for n in Note.query.order_by(Note.id.asc()).all()
    ]

    return jsonify({"users": users, "notes": notes}), 200


@dev_bp.post("/dev/seed")
def seed_demo():
    if current_app.config.get("ENV", "production") == "production":
        return jsonify({"error": "not found"}), 404

    payload = request.get_json(silent=True) or {}
    password = payload.get("password") or "password123"

    users = [
        ("demo1@test.com", "Demo User 1"),
        ("demo2@test.com", "Demo User 2"),
    ]

    created = {"users": [], "notes": []}
    for email, title_prefix in users:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, password_hash=pbkdf2_sha256.hash(password))
            db.session.add(user)
            db.session.flush()
            created["users"].append({"id": user.id, "email": user.email})

        note = Note.query.filter_by(user_id=user.id, title=f"{title_prefix} Note").first()
        if not note:
            note = Note(user_id=user.id, title=f"{title_prefix} Note", content="Seeded content")
            db.session.add(note)
            db.session.flush()
            created["notes"].append({"id": note.id, "user_id": user.id})

    db.session.commit()
    return jsonify({"seeded": created}), 201
