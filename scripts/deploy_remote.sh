#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${APP_NAME:-flaskfort}"
APP_PORT="${APP_PORT:-8000}"
IMAGE="${IMAGE:-}"
ENV_FILE="${ENV_FILE:-/opt/flaskfort/.env}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:${APP_PORT}/healthz}"

if [[ -z "$IMAGE" ]]; then
  echo "IMAGE is required (e.g. ghcr.io/org/repo:v1.0.0)" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required on the server" >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required on the server for health checks" >&2
  exit 1
fi

echo "Pulling image: $IMAGE"
for i in {1..6}; do
  if docker pull "$IMAGE"; then
    break
  fi
  echo "Pull failed, retrying in 5s..."
  sleep 5
done

PREV_IMAGE="$(docker inspect --format='{{.Config.Image}}' "$APP_NAME" 2>/dev/null || true)"

docker stop "$APP_NAME" 2>/dev/null || true
docker rm "$APP_NAME" 2>/dev/null || true

echo "Starting new container..."
docker run -d \
  --name "$APP_NAME" \
  --restart unless-stopped \
  -p "${APP_PORT}:8000" \
  --env-file "$ENV_FILE" \
  "$IMAGE"

echo "Health check: $HEALTH_URL"
for _ in {1..10}; do
  if curl -fsS "$HEALTH_URL" >/dev/null; then
    echo "Deployment healthy."
    exit 0
  fi
  sleep 3
done

echo "Health check failed, rolling back..." >&2
docker logs "$APP_NAME" --tail 200 || true
docker stop "$APP_NAME" 2>/dev/null || true
docker rm "$APP_NAME" 2>/dev/null || true

if [[ -n "$PREV_IMAGE" ]]; then
  echo "Restoring previous image: $PREV_IMAGE"
  docker pull "$PREV_IMAGE" || true
  docker run -d \
    --name "$APP_NAME" \
    --restart unless-stopped \
    -p "${APP_PORT}:8000" \
    --env-file "$ENV_FILE" \
    "$PREV_IMAGE"
else
  echo "No previous image available to roll back to." >&2
fi

exit 1
