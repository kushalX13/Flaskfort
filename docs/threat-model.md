# Threat Model (1-page)

## Scope

- Flask API for auth + notes CRUD
- JWT-based authentication
- Postgres/SQLite storage

## Assets

- User credentials (password hashes)
- JWT tokens
- Notes content
- Database availability/integrity

## Actors

- Legitimate authenticated user
- Malicious user with account
- Unauthenticated attacker on the internet

## Entry Points

- `/auth/register`
- `/auth/login`
- `/notes/*` (JWT protected)
- `/healthz`

## Key Threats and Mitigations

- **Credential stuffing / brute force**
  - Mitigation: password length checks; JWT auth
  - Future: rate limiting, MFA
- **Unauthorized note access**
  - Mitigation: user_id scoping on all note queries
- **Token leakage**
  - Mitigation: short-lived tokens (future), HTTPS in deployment
- **SQL injection**
  - Mitigation: SQLAlchemy ORM queries
- **Dependency/Container vulnerabilities**
  - Mitigation: pip-audit + trivy gates in CI
- **Accidental secret commits**
  - Mitigation: gitleaks gate in CI

## Residual Risks

- No refresh token rotation yet
- No rate limiting yet
- No audit logging beyond basic request logs
