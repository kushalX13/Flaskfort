from flask import Blueprint, render_template

ui_bp = Blueprint("ui", __name__)


@ui_bp.get("/")
def index():
    return render_template("index.html")


@ui_bp.get("/login")
def login_page():
    return render_template("login.html")


@ui_bp.get("/notes-ui")
def notes_page():
    return render_template("notes.html")
