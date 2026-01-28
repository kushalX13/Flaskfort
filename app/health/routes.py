from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.get("/healthz")
def healthz():
    # quick DB check (works for sqlite/postgres)
    db.session.execute(text("SELECT 1"))
    return jsonify({"status": "ok"}), 200
