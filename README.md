# HR Counselor

Система анализа резюме и помощи HR-специалистам в подборе персонала с использованием ИИ.

## Наша идея 

Проект представляет собой автоматизированную систему рекрутинга с поддержкой искусственного интеллекта. Цель - сократить время, необходимое для найма. Система включает анализ резюме, управление вакансиями и кандидатами.

## Технологический стек

**Backend:**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1f425f?style=flat&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-663399?style=flat&logo=python&logoColor=white)

## Компоненты проекта

| Компонент | Описание | Документация |
|-----------|----------|--------------|
| Backend   | FastAPI backend с REST API и интеграцией с внешними AI API | 📄 [backend/README.md](backend/README.md) |

## 📁 Структура проекта

```
counselor/
├── backend/                        # Backend приложение
│   ├── src/
│   │   ├── api/                    # FastAPI приложение
│   │   │   ├── app.py              # Основное приложение
│   │   │   └── __main__.py         # Точка входа
│   │   ├── config.py               # Конфигурация
│   │   ├── config_schema.py        # Схема конфигурации
│   │   ├── modules/                # Модули бизнес-логики
│   │   │   ├── users/              # Пользователи и аутентификация
│   │   │   ├── cv/                 # Управление резюме
│   │   │   ├── jobs/               # Управление вакансиями
│   │   │   ├── courses/            # Управление курсами
│   │   │   ├── folders/            # Управление папками
│   │   │   ├── generation/         # ИИ генерация и анализ
│   │   │   └── landing/            # Главная страница
│   │   ├── storages/               # Работа с данными
│   │   │   └── sql/                # SQL модели и зависимости
│   │   └── utils/                  # Утилиты
│   │       ├── security.py         # JWT и безопасность
│   │       └── file_storage.py     # Работа с файлами
│   ├── alembic/                    # Миграции базы данных
│   │   └── versions/               # Файлы миграций
│   ├── scripts/                    # Служебные скрипты
│   ├── t1hack/                     # Bruno API тесты
│   ├── uploads/                    # Загруженные файлы
│   ├── settings.yaml               # Настройки приложения
│   ├── pyproject.toml              # Зависимости и настройки проекта
│   └── uv.lock                     # Файл блокировки зависимостей
└── README.md                       # Документация проекта
```