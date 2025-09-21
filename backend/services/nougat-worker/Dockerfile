FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential poppler-utils tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY server.py .

ENV API_TOKEN=changeme
ENV MAX_FILE_MB=25
ENV NOUGAT_BIN=nougat

EXPOSE 8080
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8080"]