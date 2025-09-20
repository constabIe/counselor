#!/usr/bin/env python3
"""
Скрипт для проверки созданных пользователей и CV
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import select
from sqlalchemy import desc

from src.config import settings
from src.storages.sql.models import User, CV, UserRole


async def check_users_and_cvs():
    """Проверяет созданных пользователей и их CV"""
    
    print("🔍 Проверяем созданных пользователей и CV...")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=False
    )
    
    try:
        async with AsyncSession(engine) as session:
            # Получаем всех пользователей
            users_stmt = select(User).order_by(User.created_at.desc()) # type: ignore
            users_result = await session.execute(users_stmt)
            users = users_result.scalars().all()
            
            print(f"\n👥 Всего пользователей в базе: {len(users)}")
            print("-" * 60)
            
            for i, user in enumerate(users, 1):
                role_emoji = "👤" if user.role == UserRole.USER else "👔" if user.role == UserRole.HR else "👑"
                print(f"{i:2}. {role_emoji} {user.full_name}")
                print(f"    📧 {user.email}")
                print(f"    🎯 Роль: {user.role.value}")
                print(f"    ⭐ XP: {user.xp}")
                print(f"    📅 Создан: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Получаем CV пользователя
                cv_stmt = select(CV).where(CV.user_id == user.id, CV.is_active == True)
                cv_result = await session.execute(cv_stmt)
                cvs = cv_result.scalars().all()
                
                if cvs:
                    for cv in cvs:
                        print(f"    📄 CV: {cv.original_filename}")
                        print(f"       📂 Файл: {cv.filename}")
                        print(f"       📊 Статус анализа: {cv.analysis_status}")
                        if cv.experience_years:
                            print(f"       💼 Опыт: {cv.experience_years} лет")
                        if cv.rating:
                            print(f"       ⭐ Рейтинг: {cv.rating}/10")
                        if cv.department:
                            print(f"       🏢 Отдел: {cv.department}")
                        if cv.grade:
                            print(f"       📈 Грейд: {cv.grade}")
                        if cv.specialization:
                            print(f"       🎯 Специализация: {cv.specialization}")
                else:
                    print(f"    📄 CV: не загружено")
                
                print()
            
            # Статистика по CV
            all_cvs_stmt = select(CV).where(CV.is_active == True)
            all_cvs_result = await session.execute(all_cvs_stmt)
            all_cvs = all_cvs_result.scalars().all()
            
            print(f"📊 Статистика CV:")
            print(f"   📄 Всего активных CV: {len(all_cvs)}")
            
            if all_cvs:
                # Статистика по отделам
                departments = {}
                grades = {}
                ratings = []
                
                for cv in all_cvs:
                    if cv.department:
                        departments[cv.department] = departments.get(cv.department, 0) + 1
                    if cv.grade:
                        grades[cv.grade] = grades.get(cv.grade, 0) + 1
                    if cv.rating:
                        ratings.append(cv.rating)
                
                if departments:
                    print(f"\n📈 По отделам:")
                    for dept, count in departments.items():
                        print(f"   🏢 {dept}: {count}")
                
                if grades:
                    print(f"\n📊 По грейдам:")
                    for grade, count in grades.items():
                        print(f"   📈 {grade}: {count}")
                
                if ratings:
                    avg_rating = sum(ratings) / len(ratings)
                    print(f"\n⭐ Средний рейтинг: {avg_rating:.2f}/10")
                    print(f"   📊 Мин: {min(ratings):.1f}, Макс: {max(ratings):.1f}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_users_and_cvs())
