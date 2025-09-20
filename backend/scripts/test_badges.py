#!/usr/bin/env python3
"""
Простой тест системы бейджей
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import settings
from src.modules.badges import service as badge_service

async def test_badge_system():
    """Тестирует систему бейджей"""
    
    print("🧪 Тестирование системы бейджей...")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=False
    )
    
    try:
        async with AsyncSession(engine) as session:
            # Создаем тестового пользователя или используем существующего
            from uuid import uuid4
            test_user_id = uuid4()
            
            print(f"👤 Тестовый пользователь: {test_user_id}")
            
            # Тестируем разные триггеры
            triggers = [
                "user_registered",
                "cv_uploaded", 
                "course_enrolled",
                "course_completed"
            ]
            
            for trigger in triggers:
                print(f"\n🎯 Тестируем триггер: {trigger}")
                badges = await badge_service.badge_service.check_and_award_badges(
                    session, test_user_id, trigger
                )
                print(f"   Выдано бейджей: {len(badges)}")
                for badge in badges:
                    print(f"   🏆 {badge}")
            
            # Получаем статистику
            print(f"\n📊 Получаем статистику бейджей...")
            stats = await badge_service.badge_service.get_user_badge_stats(session, test_user_id)
            print(f"   Всего бейджей: {stats.earned_badges}/{stats.total_badges}")
            print(f"   XP от бейджей: {stats.total_xp_from_badges}")
            print(f"   Процент выполнения: {stats.completion_percentage:.1f}%")
            
            await session.rollback()  # Откатываем тестовые изменения
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        raise
    finally:
        await engine.dispose()
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(test_badge_system())
