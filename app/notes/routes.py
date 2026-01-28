from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Note

notes_bp = Blueprint("notes", __name__)


def _current_user_id() -> int:
    # stored as string in token; normalize to int
    return int(get_jwt_identity())


@notes_bp.get("")
@jwt_required()
def list_notes():
    user_id = _current_user_id()
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.id.desc()).all()
    return jsonify([n.to_dict() for n in notes]), 200


@notes_bp.post("")
@jwt_required()
def create_note():
    user_id = _current_user_id()
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = data.get("content")

    if not title:
        return jsonify({"error": "title required"}), 400

    note = Note(user_id=user_id, title=title, content=content)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@notes_bp.get("/<int:note_id>")
@jwt_required()
def get_note(note_id: int):
    user_id = _current_user_id()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"error": "not found"}), 404
    return jsonify(note.to_dict()), 200


@notes_bp.put("/<int:note_id>")
@jwt_required()
def update_note(note_id: int):
    user_id = _current_user_id()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"error": "not found"}), 404

    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "title cannot be empty"}), 400
        note.title = title
    if "content" in data:
        note.content = data.get("content")

    db.session.commit()
    return jsonify(note.to_dict()), 200


@notes_bp.delete("/<int:note_id>")
@jwt_required()
def delete_note(note_id: int):
    user_id = _current_user_id()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"error": "not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"deleted": True}), 200
