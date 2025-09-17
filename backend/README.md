# Counselor Backend

Простое FastAPI приложение для проекта Counselor.

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите сервер:
```bash
python __main__.py
```

Или:
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Главная страница с приветствием
- `GET /health` - Проверка здоровья сервиса  
- `GET /api/hello` - Приветствие на API роуте

## Доступ

После запуска API будет доступно по адресу:
- http://localhost:8000
- Документация: http://localhost:8000/docs
