#!/usr/bin/env python3
"""
Скрипт для добавления 10 пользователей и 10 CV в базу данных
"""

import asyncio
import sys
import os
import json
import random
from pathlib import Path
from uuid import uuid4
from datetime import datetime

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import select

from src.config import settings
from src.storages.sql.models import User, CV, UserRole
from src.modules.users import repository as user_repo
from src.modules.cv import repository as cv_repo


# Данные для создания пользователей
USERS_DATA = [
    {
        "email": "ivan.petrov@example.com",
        "password": "password123",
        "full_name": "Иван Петров",
        "role": UserRole.USER
    },
    {
        "email": "maria.sidorova@example.com", 
        "password": "password123",
        "full_name": "Мария Сидорова",
        "role": UserRole.USER
    },
    {
        "email": "alex.kozlov@example.com",
        "password": "password123", 
        "full_name": "Александр Козлов",
        "role": UserRole.USER
    },
    {
        "email": "elena.novikova@example.com",
        "password": "password123",
        "full_name": "Елена Новикова", 
        "role": UserRole.USER
    },
    {
        "email": "dmitry.volkov@example.com",
        "password": "password123",
        "full_name": "Дмитрий Волков",
        "role": UserRole.USER
    },
    {
        "email": "anna.morozova@example.com",
        "password": "password123",
        "full_name": "Анна Морозова",
        "role": UserRole.USER
    },
    {
        "email": "sergey.fedorov@example.com",
        "password": "password123",
        "full_name": "Сергей Федоров", 
        "role": UserRole.USER
    },
    {
        "email": "olga.romanova@example.com",
        "password": "password123",
        "full_name": "Ольга Романова",
        "role": UserRole.USER
    },
    {
        "email": "pavel.smirnov@example.com",
        "password": "password123",
        "full_name": "Павел Смирнов",
        "role": UserRole.USER
    },
    {
        "email": "tatiana.kuznetsova@example.com",
        "password": "password123",
        "full_name": "Татьяна Кузнецова",
        "role": UserRole.HR
    }
]

# Примеры данных для CV
CV_TEMPLATES = [
    {
        "skills": json.dumps(["Python", "Django", "PostgreSQL", "Docker", "Git"]),
        "experience_years": 3,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "МГУ",
            "faculty": "Факультет вычислительной математики и кибернетики",
            "graduation_year": 2021
        }),
        "current_role": json.dumps({
            "position": "Backend Developer",
            "company": "Tech Solutions"
        }),
        "age": 25,
        "department": "IT",
        "grade": "Middle",
        "specialization": "Backend Development",
        "rating": 8.5,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2"}
        ])
    },
    {
        "skills": json.dumps(["React", "TypeScript", "Node.js", "MongoDB", "AWS"]),
        "experience_years": 5,
        "education": json.dumps({
            "degree": "Магистр", 
            "university": "МФТИ",
            "faculty": "Факультет инноваций и высоких технологий",
            "graduation_year": 2019
        }),
        "current_role": json.dumps({
            "position": "Frontend Developer",
            "company": "Digital Agency"
        }),
        "age": 28,
        "department": "IT",
        "grade": "Senior",
        "specialization": "Frontend Development",
        "rating": 9.2,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "C1"}
        ])
    },
    {
        "skills": json.dumps(["Java", "Spring Boot", "Kubernetes", "Microservices", "Jenkins"]),
        "experience_years": 7,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "СПбГУ",
            "faculty": "Математико-механический факультет",
            "graduation_year": 2017
        }),
        "current_role": json.dumps({
            "position": "Senior Java Developer",
            "company": "Enterprise Solutions"
        }),
        "age": 30,
        "department": "IT",
        "grade": "Senior",
        "specialization": "Enterprise Development",
        "rating": 9.0,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2"},
            {"language": "Немецкий", "level": "A2"}
        ])
    },
    {
        "skills": json.dumps(["Data Analysis", "Python", "SQL", "Tableau", "Machine Learning"]),
        "experience_years": 4,
        "education": json.dumps({
            "degree": "Магистр",
            "university": "ВШЭ", 
            "faculty": "Факультет экономических наук",
            "graduation_year": 2020
        }),
        "current_role": json.dumps({
            "position": "Data Analyst",
            "company": "Analytics Corp"
        }),
        "age": 26,
        "department": "Analytics",
        "grade": "Middle+",
        "specialization": "Data Science",
        "rating": 8.7,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2+"}
        ])
    },
    {
        "skills": json.dumps(["DevOps", "AWS", "Terraform", "Ansible", "Linux"]),
        "experience_years": 6,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "МИРЭА",
            "faculty": "Институт информационных технологий",
            "graduation_year": 2018
        }),
        "current_role": json.dumps({
            "position": "DevOps Engineer",
            "company": "Cloud Systems"
        }),
        "age": 29,
        "department": "IT",
        "grade": "Senior",
        "specialization": "DevOps",
        "rating": 8.9,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2"}
        ])
    },
    {
        "skills": json.dumps(["QA", "Selenium", "TestRail", "Postman", "SQL"]),
        "experience_years": 2,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "ИТМО",
            "faculty": "Факультет программной инженерии и компьютерной техники",
            "graduation_year": 2022
        }),
        "current_role": json.dumps({
            "position": "QA Engineer",
            "company": "Testing Solutions"
        }),
        "age": 24,
        "department": "QA",
        "grade": "Junior+",
        "specialization": "Manual Testing",
        "rating": 7.8,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B1"}
        ])
    },
    {
        "skills": json.dumps(["Product Management", "Agile", "JIRA", "Analytics", "User Research"]),
        "experience_years": 5,
        "education": json.dumps({
            "degree": "Магистр",
            "university": "МГУ",
            "faculty": "Экономический факультет",
            "graduation_year": 2019
        }),
        "current_role": json.dumps({
            "position": "Product Manager",
            "company": "Product Company"
        }),
        "age": 27,
        "department": "Product",
        "grade": "Middle+",
        "specialization": "Product Management",
        "rating": 8.6,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "C1"}
        ])
    },
    {
        "skills": json.dumps(["UI/UX Design", "Figma", "Adobe Creative Suite", "Prototyping", "User Research"]),
        "experience_years": 4,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "МГХПА им. С.Г. Строганова",
            "faculty": "Факультет дизайна",
            "graduation_year": 2020
        }),
        "current_role": json.dumps({
            "position": "UX/UI Designer",
            "company": "Design Studio"
        }),
        "age": 26,
        "department": "Design",
        "grade": "Middle",
        "specialization": "UX/UI Design",
        "rating": 8.4,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2"}
        ])
    },
    {
        "skills": json.dumps(["Marketing", "Google Analytics", "SEO", "Content Marketing", "Social Media"]),
        "experience_years": 3,
        "education": json.dumps({
            "degree": "Бакалавр",
            "university": "РГГУ",
            "faculty": "Факультет журналистики",
            "graduation_year": 2021
        }),
        "current_role": json.dumps({
            "position": "Marketing Specialist",
            "company": "Marketing Agency"
        }),
        "age": 25,
        "department": "Marketing",
        "grade": "Middle-",
        "specialization": "Digital Marketing",
        "rating": 7.9,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "B2"},
            {"language": "Французский", "level": "A2"}
        ])
    },
    {
        "skills": json.dumps(["HR", "Recruitment", "Employee Relations", "HRIS", "Performance Management"]),
        "experience_years": 8,
        "education": json.dumps({
            "degree": "Магистр",
            "university": "СПбГУ",
            "faculty": "Факультет психологии",
            "graduation_year": 2016
        }),
        "current_role": json.dumps({
            "position": "HR Manager",
            "company": "HR Solutions"
        }),
        "age": 32,
        "department": "HR",
        "grade": "Senior",
        "specialization": "Talent Management",
        "rating": 9.1,
        "languages": json.dumps([
            {"language": "Русский", "level": "Родной"},
            {"language": "Английский", "level": "C1"}
        ])
    }
]


async def create_users_and_cvs():
    """Создает пользователей и CV"""
    
    print("🚀 Начинаем создание пользователей и CV...")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=False
    )
    
    try:
        async with AsyncSession(engine) as session:
            created_users_data = []
            
            # Создаем пользователей
            print("\n👥 Создаем пользователей...")
            for i, user_data in enumerate(USERS_DATA, 1):
                try:
                    # Проверяем, не существует ли пользователь с таким email
                    existing_user = await user_repo.get_user_by_email(session, user_data["email"])
                    if existing_user:
                        print(f"   {i}. ⚠️  Пользователь {user_data['email']} уже существует, пропускаем")
                        created_users_data.append({
                            "id": existing_user.id,
                            "full_name": existing_user.full_name,
                            "email": existing_user.email
                        })
                        continue
                    
                    user = await user_repo.create_user(
                        session,
                        email=user_data["email"],
                        password=user_data["password"],
                        full_name=user_data["full_name"],
                        role=user_data["role"]
                    )
                    
                    # Сохраняем данные пользователя в простом словаре
                    created_users_data.append({
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email
                    })
                    print(f"   {i}. ✅ Создан пользователь: {user.full_name} ({user.email})")
                    
                except Exception as e:
                    print(f"   {i}. ❌ Ошибка создания пользователя {user_data['email']}: {e}")
                    continue
            
            await session.commit()
            print(f"\n✅ Создано пользователей: {len(created_users_data)}")
            
            # Получаем список существующих файлов CV
            uploads_dir = project_root / "uploads" / "cvs"
            existing_files = list(uploads_dir.glob("*.pdf")) if uploads_dir.exists() else []
            
            if not existing_files:
                print("⚠️  Нет файлов PDF в директории uploads/cvs для создания CV")
                return
            
            # Создаем CV для первых 10 пользователей
            print(f"\n📄 Создаем CV (доступно файлов: {len(existing_files)})...")
            
            cv_count = 0
            for i, (user_data, cv_template) in enumerate(zip(created_users_data[:10], CV_TEMPLATES), 1):
                # Получаем данные пользователя из словаря
                user_full_name = user_data["full_name"]
                user_id = user_data["id"]
                
                try:
                    # Выбираем случайный файл или создаем новый UUID
                    if existing_files and i <= len(existing_files):
                        file_path = existing_files[i-1]
                        filename = file_path.name
                        file_size = file_path.stat().st_size if file_path.exists() else 1024
                        actual_file_path = str(file_path.relative_to(project_root))
                    else:
                        # Создаем новый filename если файлов недостаточно
                        filename = f"{uuid4()}.pdf"
                        file_size = 1024
                        actual_file_path = f"uploads/cvs/{filename}"
                    
                    original_filename = f"CV_{user_full_name.replace(' ', '_')}.pdf"
                    
                    # Проверяем, есть ли уже активное CV у пользователя
                    active_cv_count = await cv_repo.get_user_active_cv_count(session, user_id)
                    if active_cv_count > 0:
                        print(f"   {i}. ⚠️  У пользователя {user_full_name} уже есть активное CV, пропускаем")
                        continue
                    
                    cv = await cv_repo.create_cv(
                        session=session,
                        user_id=user_id,
                        filename=filename,
                        original_filename=original_filename,
                        file_path=actual_file_path,
                        file_size=file_size,
                        content_type="application/pdf",
                        parsed_text=f"Резюме кандидата {user_full_name}. Опыт работы {cv_template['experience_years']} лет.",
                        skills=cv_template["skills"],
                        experience_years=cv_template["experience_years"],
                        education=cv_template["education"],
                        current_role=cv_template["current_role"],
                        age=cv_template["age"],
                        department=cv_template["department"],
                        grade=cv_template["grade"],
                        specialization=cv_template["specialization"],
                        rating=cv_template["rating"],
                        languages=cv_template["languages"],
                        analysis_status="completed"
                    )
                    
                    cv_count += 1
                    print(f"   {i}. ✅ Создано CV для {user_full_name}: {original_filename}")
                    
                except Exception as e:
                    print(f"   {i}. ❌ Ошибка создания CV для {user_full_name}: {e}")
                    continue
            
            await session.commit()
            print(f"\n✅ Создано CV: {cv_count}")
            
            # Выводим статистику
            print(f"\n📊 Итоговая статистика:")
            print(f"   👥 Пользователей: {len(created_users_data)}")
            print(f"   📄 CV: {cv_count}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_users_and_cvs())
