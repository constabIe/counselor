# HR Counselor Backend

Система для анализа резюме и помощи HR-специалистам в подборе персонала.

## Требования

- Python 3.11+
- PostgreSQL 15+
- [uv](https://docs.astral.sh/uv/) - современный менеджер пакетов Python

## Быстрый старт

### 1. Установка uv (если не установлен)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Создание и активация виртуального окружения

```bash
# Создание окружения с Python 3.11+
uv python install 3.11
uv venv --python 3.11

# Активация окружения
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
# Установка всех зависимостей из pyproject.toml
uv sync

# Или установка только основных зависимостей
uv pip install -e .
```

### 4. Настройка конфигурации

Создайте и Отредактируйте файл `settings.yaml` под ваши нужды по примеру `settings.example.yaml`.


### 5. Инициализация базы данных

```bash
# Создание таблиц (временное решение)
uv run python init_db.py

```

### 6. Запуск сервера

```bash
# Для разработки
uv run python -m src.api

# Или через uvicorn напрямую
uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```


## Структура проекта

```
backend/
├── src/
│   ├── api/                    # FastAPI приложение
│   │   ├── app.py             # Основное приложение
│   │   └── __main__.py        # Точка входа
│   ├── config.py              # Конфигурация
│   ├── config_schema.py       # Схема конфигурации  
│   ├── modules/               # Модули бизнес-логики
│   │   ├── users/             # Пользователи и аутентификация
│   │   ├── cv/                # Управление резюме
│   │   └── landing/           # Главная страница
│   ├── storages/              # Работа с данными
│   │   └── sql/               # SQL модели и зависимости
│   └── utils/                 # Утилиты
│       ├── security.py        # JWT и безопасность
│       └── file_storage.py    # Работа с файлами
├── uploads/                   # Загруженные файлы
├── t1hack/                    # Bruno API тесты
├── settings.yaml              # Настройки приложения
├── pyproject.toml            # Зависимости и настройки проекта
├── uv.lock                   # Файл блокировки зависимостей
├── init_db.py               # Инициализация БД
└── migrate_cv_fields.py     # Миграция новых полей CV
```

