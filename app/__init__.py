import logging

from dotenv import load_dotenv
from flask import Flask, request

from app.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_object: type[Config] = Config) -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    from app import models  # noqa: F401

    # Logging (basic “audit-ish” request logs)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    @app.before_request
    def log_request():
        app.logger.info(
            "req method=%s path=%s ip=%s",
            request.method,
            request.path,
            request.headers.get("X-Forwarded-For", request.remote_addr),
        )

    # Blueprints
    from app.auth.routes import auth_bp
    from app.ai.routes import ai_bp
    from app.dev.routes import dev_bp
    from app.docs.routes import docs_bp
    from app.health.routes import health_bp
    from app.notes.routes import notes_bp
    from app.ui.routes import ui_bp

    app.register_blueprint(ui_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(health_bp)
    app.register_blueprint(dev_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(ai_bp)

    return app
