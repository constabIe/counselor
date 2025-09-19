#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from src.storages.sql.models import SQLModel
# Импортируем модели для их регистрации
from src.storages.sql.models import User, RefreshToken, CV


async def init_db():
    """Создает таблицы в базе данных"""
    print(f"Инициализация базы данных: {settings.db_url.get_secret_value()}")
    
    engine = create_async_engine(
        settings.db_url.get_secret_value(),
        echo=True
    )
    
    try:
        async with engine.begin() as conn:
            # Удаляем все таблицы (осторожно!)
            print("Удаляем существующие таблицы...")
            await conn.run_sync(SQLModel.metadata.drop_all)
            
            # Создаем все таблицы
            print("Создаем новые таблицы...")
            await conn.run_sync(SQLModel.metadata.create_all)
        
        print("✅ База данных успешно инициализирована!")
        
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
