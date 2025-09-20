#!/usr/bin/env python3
"""
Тест расширенной системы XP для CV
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import settings

async def test_cv_xp_system():
    """Тестирует систему XP для CV"""
    
    print("🧪 Тестирование расширенной системы XP для CV...")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=False
    )
    
    try:
        async with AsyncSession(engine) as session:
            from uuid import uuid4
            from src.modules.cv.routes import calculate_cv_update_xp
            
            # Тестируем расчет XP за обновление различных полей
            test_cases = [
                # Простые поля
                {"age": 25},
                {"comments": "Отличный кандидат"},
                
                # Средние поля
                {"languages": '["English", "Russian"]'},
                {"department": "IT"},
                
                # Важные поля
                {"skills": '["Python", "FastAPI", "SQL"]'},
                {"education": '{"degree": "Bachelor", "university": "MSU"}'},
                {"jobs": '[{"company": "Tech Corp", "position": "Developer"}]'},
                
                # Множественные поля (с бонусом)
                {
                    "skills": '["Python", "FastAPI"]',
                    "experience_years": 3,
                    "education": '{"degree": "Bachelor"}',
                    "languages": '["English"]',
                    "department": "IT"
                },
                
                # Много полей (больший бонус)
                {
                    "skills": '["Python"]',
                    "experience_years": 5,
                    "education": '{"degree": "Master"}',
                    "jobs": '[{"company": "ABC"}]',
                    "languages": '["English", "German"]',
                    "department": "Engineering",
                    "age": 30,
                    "comments": "Great candidate"
                }
            ]
            
            print("\n📊 Тестирование расчета XP за обновления CV:")
            for i, fields in enumerate(test_cases, 1):
                xp = calculate_cv_update_xp(fields)
                field_names = list(fields.keys())
                print(f"   {i}. Поля: {field_names}")
                print(f"      XP: {xp}")
                print()
            
            print("✅ Тестирование расчета XP завершено!")
            
            # Показываем таблицу XP значений
            print("\n💰 Таблица XP за различные поля CV:")
            from src.modules.cv.routes import CV_FIELD_XP_VALUES
            for field, xp in sorted(CV_FIELD_XP_VALUES.items(), key=lambda x: x[1], reverse=True):
                print(f"   {field:20} -> {xp} XP")
            
            print(f"\n🎯 Бонусы за множественные обновления:")
            print(f"   3+ полей -> +2 XP")
            print(f"   5+ полей -> +5 XP")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        raise
    finally:
        await engine.dispose()
    
    print("\n✅ Все тесты завершены!")

if __name__ == "__main__":
    asyncio.run(test_cv_xp_system())
