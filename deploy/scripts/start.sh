#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 2
done

echo "Alembic migrations..."
uv run alembic upgrade head

echo "Application launch..."
exec uv run uvicorn src.api.app:app --host "$HOST" --port "$PORT"