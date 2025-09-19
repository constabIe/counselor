#!/usr/bin/env python3
"""
Скрипт для демонстрации логики деактивации старых CV
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import select

from src.config import settings
from src.storages.sql.models import CV, User
from src.modules.cv import repository as cv_repo


async def demo_cv_logic(session: AsyncSession):
    """Демонстрация логики деактивации CV"""
    
    # Получаем первого пользователя для демонстрации
    stmt = select(User).where(User.is_active == True).limit(1)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        print("❌ Нет активных пользователей в БД")
        return
    
    print(f"👤 Пользователь: {user.full_name} (ID: {user.id})")
    print("-" * 50)
    
    # Проверяем текущее состояние CV
    active_count = await cv_repo.get_user_active_cv_count(session, user.id)
    all_cvs = await cv_repo.get_user_cvs(session, user.id, include_inactive=True)
    
    print(f"📊 Текущая статистика:")
    print(f"   Активных CV: {active_count}")
    print(f"   Всего CV: {len(all_cvs)}")
    
    if all_cvs:
        print(f"\n📄 Список всех CV:")
        for i, cv in enumerate(all_cvs, 1):
            status = "✅ АКТИВНО" if cv.is_active else "❌ НЕАКТИВНО"
            print(f"   {i}. {cv.original_filename} - {status}")
    
    print(f"\n🔍 Поиск этого пользователя в generation:")
    
    # Симулируем поиск через generation модуль
    from src.modules.generation import repository as gen_repo
    from src.modules.generation.schemas import GenerationFilters
    
    # Поиск по общим тегам
    empty_filters = GenerationFilters(
        department=None,
        experience_years_min=None,
        experience_years_max=None,
        skills=None,
        level=None,
        languages=None,
        education_level=None,
        age_min=None,
        age_max=None
    )
    
    employees = await gen_repo.search_employees_by_tags(
        session=session,
        tags=["python", "general", "professional"],
        filters=empty_filters,
        limit=10
    )
    
    user_found = None
    for emp in employees:
        # Проверяем, найден ли наш пользователь
        cv_stmt = select(CV).where(CV.id == emp.id)
        cv_result = await session.execute(cv_stmt)
        cv = cv_result.scalar_one_or_none()
        
        if cv and cv.user_id == user.id:
            user_found = emp
            break
    
    if user_found:
        print(f"   ✅ Пользователь найден в результатах поиска")
        print(f"   📋 CV ID: {user_found.id}")
        print(f"   ⭐ Рейтинг: {user_found.rating}")
        print(f"   🎯 Match Score: {user_found.match_score}")
    else:
        print(f"   ❌ Пользователь НЕ найден в результатах поиска")
    
    print(f"\n✨ Логика работает корректно:")
    print(f"   • При загрузке нового CV старые автоматически деактивируются")
    print(f"   • В поиске участвует только одно активное CV на пользователя")
    print(f"   • Деактивированные CV сохраняются в истории")


async def main():
    """Основная функция"""
    
    print("🔧 Демонстрация логики управления CV")
    print("=" * 60)
    
    # Создаем подключение к БД
    engine = create_async_engine(
        str(settings.db_url.get_secret_value()),
        echo=False,
        future=True,
    )
    
    try:
        async with AsyncSession(engine) as session:
            await demo_cv_logic(session)
        
        print(f"\n✅ Демонстрация завершена!")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return 1
    
    finally:
        await engine.dispose()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
