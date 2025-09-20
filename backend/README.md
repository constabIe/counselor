# 🚀 HR Counselor Backend

> Высокопроизводительный backend API для системы анализа резюме и автоматизации процессов подбора персонала с использованием ИИ.

## ✨ Возможности

- **Аутентификация и авторизация** - JWT токены, безопасная работа с пользователями
- **Управление резюме** - загрузка, анализ и обработка CV с помощью ИИ
- **Система вакансий** - создание, публикация и управление job positions
- **Образовательная платформа** - курсы повышения квалификации и система опыта
- **Система достижений** - badges и геймификация процесса обучения
- **Организация данных** - папки для структурирования резюме и вакансий

## 🔧 Технологический стек


![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-migrations-663399?style=flat&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/UV-package_manager-yellow?style=flat&logo=python&logoColor=white)
![AsyncPG](https://img.shields.io/badge/AsyncPG-async_driver-blue?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-validation-red?style=flat)

## 🚀 Быстрый старт

### Требования

- Python 3.13+
- PostgreSQL 15+
- [uv](https://docs.astral.sh/uv/) - современный менеджер пакетов Python

### Установка

1. **Установка uv** (если не установлен):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Создание виртуального окружения**:
   ```bash
   uv python install 3.13
   uv venv --python 3.13
   source .venv/bin/activate  # Linux/macOS
   ```

3. **Установка зависимостей**:
   ```bash
   uv sync
   ```

4. **Настройка конфигурации**:
   ```bash
   cp settings.example.yaml settings.yaml
   # Отредактируйте settings.yaml под ваши нужды
   ```

5. **Инициализация базы данных**:
   ```bash
   uv run alembic upgrade head
   ```

6. **Запуск сервера**:
   ```bash
   # Режим разработки
   uv run python -m src.api --reload
   
   # Или через uvicorn
   uv run uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
   ```


## 📁 Структура проекта

```
backend/
├── src/
│   ├── api/                    # FastAPI приложение
│   │   ├── app.py              # Основное приложение
│   │   └── __main__.py         # Точка входа
│   ├── config.py               # Конфигурация
│   ├── config_schema.py        # Схема конфигурации
│   ├── modules/                # Модули бизнес-логики
│   │   ├── users/              # Пользователи и аутентификация
│   │   ├── cv/                 # Управление резюме
│   │   ├── jobs/               # Управление вакансиями
│   │   ├── courses/            # Управление курсами
│   │   ├── folders/            # Управление папками
│   │   ├── generation/         # ИИ генерация и анализ
│   │   └── landing/            # Главная страница
│   ├── storages/               # Работа с данными
│   │   └── sql/                # SQL модели и зависимости
│   └── utils/                  # Утилиты
│       ├── security.py         # JWT и безопасность
│       └── file_storage.py     # Работа с файлами
├── alembic/                    # Миграции базы данных
│   └── versions/               # Файлы миграций
├── scripts/                    # Служебные скрипты
│   ├── init_db.py              # Инициализация БД
│   ├── check_cvs.py            # Проверка резюме
│   └── populate_courses.py     # Заполнение курсов
├── t1hack/                     # Bruno API тесты
├── uploads/                    # Загруженные файлы
│   └── cvs/                    # PDF файлы резюме
├── settings.yaml               # Настройки приложения
├── settings.example.yaml       # Пример настроек
├── pyproject.toml              # Зависимости и настройки проекта
└── uv.lock                     # Файл блокировки зависимостей
```

## 🔌 API Документация

После запуска сервера документация доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs

## 🧪 Тестирование API

В папке `t1hack/` находятся тесты Bruno для проверки API endpoints:
- Аутентификация (`auth/`)
- Управление вакансиями (`jobs/`)
- Загрузка и управление резюме
- Работа с курсами

## 🗄️ База данных

Проект использует:
- **PostgreSQL** как основную БД
- **Alembic** для миграций
- **SQLAlchemy** как ORM
- **AsyncPG** для асинхронной работы с PostgreSQL

### Миграции

```bash
# Создание новой миграции
uv run alembic revision --autogenerate -m "description"

# Применение миграций
uv run alembic upgrade head

# Откат миграции
uv run alembic downgrade -1
```

## 🛠️ Разработка

### Полезные скрипты

```bash
# Инициализация базы данных
uv run python scripts/init_db.py

# Заполнение тестовыми курсами
uv run python scripts/populate_courses.py

# Проверка состояния базы
uv run python scripts/check_postgres.py

# Тестирование системы badges
uv run python scripts/test_badges.py
```

### Структура модулей

Каждый модуль содержит:
- `routes.py` - FastAPI роутеры и endpoints
- `models.py` - SQLAlchemy модели
- `schemas.py` - Pydantic схемы для валидации
- `service.py` - бизнес-логика
- `dependencies.py` - DI зависимости

