FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    build-essential \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./backend/pyproject.toml ./backend/uv.lock ./
RUN uv sync --frozen --no-dev

COPY ./backend .

COPY ./deploy/.env .env

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn src.api.app:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]
