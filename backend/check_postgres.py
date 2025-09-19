#!/usr/bin/env python3
"""
Скрипт для проверки подключения к PostgreSQL и создания базы данных t1
"""

import asyncio
import asyncpg
from src.config import settings


async def check_postgres_connection():
    """Проверяет подключение к PostgreSQL и создает базу данных t1 если нужно"""
    
    # Извлекаем параметры подключения из URL
    db_url = settings.db_url.get_secret_value()
    
    # Для создания базы данных подключаемся к postgres
    postgres_url = db_url.replace("/t1", "/postgres")
    
    try:
        # Подключаемся к postgres для создания базы данных
        conn = await asyncpg.connect(postgres_url.replace("postgresql+asyncpg://", "postgresql://"))
        
        # Проверяем, существует ли база данных t1
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 't1'"
        )
        
        if not result:
            print("База данных t1 не найдена. Создаем...")
            await conn.execute("CREATE DATABASE t1")
            print("✅ База данных t1 создана!")
        else:
            print("✅ База данных t1 уже существует")
        
        await conn.close()
        
        # Теперь проверяем подключение к базе t1
        t1_conn = await asyncpg.connect(db_url.replace("postgresql+asyncpg://", "postgresql://"))
        print("✅ Подключение к базе данных t1 успешно!")
        await t1_conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        print("\nУбедитесь что:")
        print("1. PostgreSQL запущен")
        print("2. Пользователь 'postgres' с паролем 'postgres' существует")
        print("3. Доступ разрешен с localhost")
        return False


if __name__ == "__main__":
    success = asyncio.run(check_postgres_connection())
    if success:
        print("\n🎉 PostgreSQL готов к работе!")
    else:
        print("\n💡 Подсказка: для быстрого запуска PostgreSQL можно использовать Docker:")
        print("docker run --name postgres-t1 -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15")
