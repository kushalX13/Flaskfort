from flask import Blueprint, jsonify, render_template, request

docs_bp = Blueprint("docs", __name__)


@docs_bp.get("/openapi.json")
def openapi():
    base_url = request.host_url.rstrip("/")
    return jsonify(
        {
            "openapi": "3.0.3",
            "info": {"title": "FlaskFort API", "version": "1.0.0"},
            "servers": [{"url": base_url}],
            "paths": {
                "/healthz": {
                    "get": {
                        "summary": "Health check",
                        "responses": {"200": {"description": "OK"}},
                    }
                },
                "/auth/register": {
                    "post": {
                        "summary": "Register",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "email": {"type": "string"},
                                            "password": {"type": "string"},
                                        },
                                        "required": ["email", "password"],
                                    }
                                }
                            },
                        },
                        "responses": {"201": {"description": "Created"}},
                    }
                },
                "/auth/login": {
                    "post": {
                        "summary": "Login",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "email": {"type": "string"},
                                            "password": {"type": "string"},
                                        },
                                        "required": ["email", "password"],
                                    }
                                }
                            },
                        },
                        "responses": {"200": {"description": "OK"}},
                    }
                },
                "/notes": {
                    "get": {
                        "summary": "List notes",
                        "security": [{"bearerAuth": []}],
                        "responses": {"200": {"description": "OK"}},
                    },
                    "post": {
                        "summary": "Create note",
                        "security": [{"bearerAuth": []}],
                        "responses": {"201": {"description": "Created"}},
                    },
                },
                "/notes/{note_id}": {
                    "get": {
                        "summary": "Get note",
                        "security": [{"bearerAuth": []}],
                        "parameters": [
                            {
                                "name": "note_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    },
                    "put": {
                        "summary": "Update note",
                        "security": [{"bearerAuth": []}],
                        "parameters": [
                            {
                                "name": "note_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    },
                    "delete": {
                        "summary": "Delete note",
                        "security": [{"bearerAuth": []}],
                        "parameters": [
                            {
                                "name": "note_id",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer"},
                            }
                        ],
                        "responses": {"200": {"description": "OK"}},
                    },
                },
            },
            "components": {
                "securitySchemes": {
                    "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
                }
            },
        }
    )


@docs_bp.get("/docs")
def docs():
    return render_template("swagger.html")
