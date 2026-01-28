import requests
from flask import Blueprint, current_app, jsonify, request

ai_bp = Blueprint("ai", __name__)


def _ollama_config():
    base_url = current_app.config.get("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = current_app.config.get("OLLAMA_MODEL", "llama3.1:8b")
    return base_url, model


def _prompt_for(action: str, title: str, content: str, user_prompt: str) -> str:
    base = f"Title: {title}\nContent: {content}\n\n"
    if action == "summarize":
        return base + "Summarize the note in 3 bullet points."
    if action == "rewrite":
        return base + "Rewrite the note clearly in professional tone."
    if action == "generate":
        return f"Create a note from this prompt:\n{user_prompt}"
    if action == "tags":
        return base + "Return 3-5 short tags, comma-separated."
    return user_prompt or base


@ai_bp.post("/ai/assist")
def assist():
    payload = request.get_json(silent=True) or {}
    action = payload.get("action") or "summarize"
    title = payload.get("title") or ""
    content = payload.get("content") or ""
    user_prompt = payload.get("prompt") or ""

    prompt = _prompt_for(action, title, content, user_prompt)
    base_url, model = _ollama_config()

    try:
        resp = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30,
        )
    except requests.RequestException:
        return jsonify({"error": "LLM request failed"}), 502

    if resp.status_code >= 400:
        return jsonify({"error": "LLM error", "detail": resp.text}), 502

    data = resp.json()
    content_out = data.get("response", "")
    return jsonify({"result": content_out}), 200
