# HR Counselor Backend

Backend API для системы анализа резюме и помощи HR-специалистам в подборе персонала.

## 🔧 Технологический стек

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1f425f?style=flat&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-663399?style=flat&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/UV-package_manager-yellow?style=flat)

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

### Миграции

```bash
# Создание новой миграции
uv run alembic revision --autogenerate -m "описание изменений"

# Применение миграций
uv run alembic upgrade head
```

