FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc libpq-dev build-essential netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Сначала копируем только зависимости, чтобы кэшировались слои
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Копируем исходники
COPY . .

# Копируем start.sh и делаем его исполняемым
COPY ../deploy/scripts/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

# Запуск через стартовый скрипт (ждём БД → применяем миграции → стартуем uvicorn)
CMD ["/start.sh"]