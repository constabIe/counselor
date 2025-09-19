#!/usr/bin/env python3
"""
Скрипт для заполнения БД курсами по умолчанию
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import select

from src.config import settings
from src.storages.sql.models import Course, CourseLevel


async def create_default_courses(session: AsyncSession):
    """Создает курсы по умолчанию"""
    
    # Проверяем, есть ли уже курсы в БД
    result = await session.execute(select(Course))
    existing_courses = result.scalars().all()
    
    if existing_courses:
        print(f"В БД уже есть {len(existing_courses)} курсов. Пропускаем создание.")
        return
    
    # Курсы по умолчанию
    default_courses = [
        {
            "title": "Основы Python для начинающих",
            "direction": "IT",
            "level": CourseLevel.BEGINNER,
            "duration_hours": 40,
            "description": "Изучение основ программирования на Python: переменные, функции, циклы, условия. Идеально для тех, кто только начинает изучать программирование."
        },
        {
            "title": "Веб-разработка с Django",
            "direction": "IT",
            "level": CourseLevel.INTERMEDIATE,
            "duration_hours": 60,
            "description": "Создание веб-приложений с использованием Django фреймворка. Изучение MVC, работа с базами данных, создание REST API."
        },
        {
            "title": "DevOps и контейнеризация",
            "direction": "IT",
            "level": CourseLevel.ADVANCED,
            "duration_hours": 80,
            "description": "Глубокое изучение DevOps практик: Docker, Kubernetes, CI/CD, мониторинг. Автоматизация развертывания и управления инфраструктурой."
        },
        {
            "title": "Основы HR-менеджмента",
            "direction": "HR",
            "level": CourseLevel.BEGINNER,
            "duration_hours": 32,
            "description": "Введение в HR: подбор персонала, адаптация, оценка эффективности, основы трудового права."
        },
        {
            "title": "Продвинутые HR-технологии",
            "direction": "HR",
            "level": CourseLevel.ADVANCED,
            "duration_hours": 56,
            "description": "Современные HR-инструменты: People Analytics, HRIS системы, геймификация в HR, управление талантами."
        },
        {
            "title": "Цифровой маркетинг",
            "direction": "Marketing",
            "level": CourseLevel.INTERMEDIATE,
            "duration_hours": 48,
            "description": "Комплексный курс по интернет-маркетингу: SEO, контекстная реклама, SMM, email-маркетинг, веб-аналитика."
        },
        {
            "title": "Проектное управление (PMP)",
            "direction": "Management",
            "level": CourseLevel.ADVANCED,
            "duration_hours": 72,
            "description": "Профессиональное управление проектами по стандартам PMI: планирование, контроль, управление рисками, командная работа."
        },
    ]
    
    print("Создаем курсы по умолчанию...")
    
    for course_data in default_courses:
        course = Course(**course_data)
        session.add(course)
        print(f"  + {course_data['title']} ({course_data['direction']}, {course_data['level']})")
    
    await session.commit()
    print(f"Создано {len(default_courses)} курсов.")


async def main():
    """Основная функция"""
    
    print("Скрипт заполнения БД курсами")
    print("=" * 50)
    
    # Создаем подключение к БД
    engine = create_async_engine(
        str(settings.db_url.get_secret_value()),
        echo=False,
        future=True,
    )
    
    try:
        async with AsyncSession(engine) as session:
            await create_default_courses(session)
        
        print("\nГотово! ✅")
        
    except Exception as e:
        print(f"\nОшибка: {e}")
        return 1
    
    finally:
        await engine.dispose()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
