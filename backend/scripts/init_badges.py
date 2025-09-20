#!/usr/bin/env python3
"""
Скрипт для инициализации предустановленных бэйджей
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import settings
from src.modules.badges import repository as badge_repo
from src.storages.sql.models import BadgeCategory

# Предустановленные бэйджи
INITIAL_BADGES = [
    # Образование
    {
        "code": "first_course",
        "name": "Ученик",
        "category": BadgeCategory.EDUCATION,
        "xp_reward": 20
    },
    {
        "code": "fast_learner", 
        "name": "Быстрый ученик",
        "category": BadgeCategory.EDUCATION, 
        "xp_reward": 50
    },
    
    # Карьера
    {
        "code": "first_cv",
        "name": "Первый шаг",
        "category": BadgeCategory.CAREER,
        "xp_reward": 15
    },
    {
        "code": "job_explorer",
        "name": "Исследователь",
        "category": BadgeCategory.CAREER,
        "xp_reward": 25
    },
    
    # Навыки
    {
        "code": "skill_master",
        "name": "Мастер навыков", 
        "category": BadgeCategory.SKILLS,
        "xp_reward": 30
    },
    
    # Активность
    {
        "code": "early_bird",
        "name": "Ранняя пташка",
        "category": BadgeCategory.ACTIVITY, 
        "xp_reward": 40
    },
    {
        "code": "profile_master",
        "name": "Мастер профиля",
        "category": BadgeCategory.ACTIVITY,
        "xp_reward": 35
    }
]


async def init_badges():
    """Создает предустановленные бэйджи"""
    
    print("🏆 Инициализация системы бэйджей...")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=False
    )
    
    try:
        async with AsyncSession(engine) as session:
            created_count = 0
            
            for badge_data in INITIAL_BADGES:
                # Проверяем, не существует ли уже бэйдж с таким кодом
                existing_badge = await badge_repo.get_badge_by_code(session, badge_data["code"])
                
                if existing_badge:
                    print(f"   ⚠️  Бэйдж '{badge_data['code']}' уже существует, пропускаем")
                    continue
                
                # Создаем новый бэйдж
                try:
                    badge = await badge_repo.create_badge(session, badge_data)
                    created_count += 1
                    print(f"   ✅ Создан бэйдж: {badge.name} ({badge.code})")
                except Exception as e:
                    print(f"   ❌ Ошибка создания бэйджа {badge_data['code']}: {e}")
                    continue
            
            await session.commit()
            print(f"\n✅ Инициализация завершена. Создано бэйджей: {created_count}")
            
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_badges())
