# 🚀 HR Counselor

> Комплексная система анализа резюме и автоматизации HR-процессов с поддержкой искусственного интеллекта.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

## 💡 Идея

Автоматизированная система рекрутинга с поддержкой ИИ для сокращения времени найма. Включает анализ резюме, интеллектуальный подбор кандидатов, управление вакансиями и образовательную платформу с системой достижений.

## 🛠️ Технологический стек

**Backend:**  
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

**Frontend:**  
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

## 🚀 Быстрый старт

### Локальная разработка

**Backend:**
```bash
cd backend
uv sync
cp settings.example.yaml settings.yaml
uv run alembic upgrade head
uv run python -m src.api --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📦 Компоненты

| Компонент | Описание | Документация |
|-----------|----------|--------------|
| **Backend** | FastAPI сервер с REST API и ИИ-интеграцией | [backend/README.md](backend/README.md) |
| **Frontend** | React приложение с современным интерфейсом | [frontend/README.md](frontend/README.md) |

## 🎯 Наша идея

**HR Counselor** - это инновационная платформа, разработанная для революционизации процессов рекрутинга и управления персоналом. Система использует передовые технологии искусственного интеллекта для:

- **Автоматического анализа резюме** и сопоставления с требованиями вакансий
- **Интеллектуального подбора кандидатов** на основе навыков и опыта
- **Предсказательной аналитики** для оценки потенциала сотрудников
- **Персонализированного обучения** и развития карьеры
- **Геймификации процессов** обучения и мотивации
