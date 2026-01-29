# FlaskFort

Secure Notes API with JWT auth, Postgres, CI, Docker, and security gates.

![CI](https://github.com/kushalX13/Flaskfort/actions/workflows/ci.yml/badge.svg)
![Security](https://github.com/kushalX13/Flaskfort/actions/workflows/security.yml/badge.svg)

## Architecture

```mermaid
flowchart LR
    Client[Client] -->|JWT| API[FlaskFort API]
    API -->|SQL| DB[(Postgres)]
```

See `docs/architecture.md` for details.

## Features

- JWT auth (register/login)
- Notes CRUD with ownership enforcement
- Health check endpoint
- Tests + linting
- Dockerized API + Postgres
- CI pipeline with security gates

## Endpoints

- `POST /auth/register` {email, password}
- `POST /auth/login` {email, password} -> JWT
- `GET /notes`
- `POST /notes`
- `GET /notes/<id>`
- `PUT /notes/<id>`
- `DELETE /notes/<id>`
- `GET /healthz`

## Local run (SQLite)

```bash
cp .env.example .env
python -m pip install -r requirements.txt -r requirements-dev.txt
flask --app wsgi.py db upgrade
flask --app wsgi.py run
```

## Docker (Postgres)

```bash
docker compose up --build
```

## Quality gate

```bash
ruff check .
pytest
```

## Security gates (CI)

- gitleaks: blocks secret leaks
- pip-audit: blocks High/Critical dependency vulns
- trivy: blocks CRITICAL container vulns

Reports are uploaded as CI artifacts on each run.

## LLM (local Ollama)

Install Ollama and pull a model:
```bash
ollama pull llama3.1:8b
```

Set in `.env`:
```
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b
```

This enables the local LLM endpoint at `POST /ai/assist` (no external billing).

## Docs

- `docs/architecture.md`
- `docs/threat-model.md`
