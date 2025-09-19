#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from sqlmodel import select
from src.storages.sql.dependencies import async_session_maker
from src.storages.sql.models import CV, User


async def check_cvs():
    """Проверяет все CV в базе данных"""
    
    async with async_session_maker() as session:
        print("=== Проверка CV в базе данных ===\n")
        
        # Получаем все CV
        stmt = select(CV)
        result = await session.execute(stmt)
        cvs = result.scalars().all()
        
        print(f"Всего CV в базе: {len(cvs)}")
        
        for cv in cvs:
            print(f"\nCV ID: {cv.id}")
            print(f"User ID: {cv.user_id}")
            print(f"Filename: {cv.filename}")
            print(f"Is Active: {cv.is_active}")
            print(f"Analysis Status: {cv.analysis_status}")
            
            # Проверяем пользователя
            user_stmt = select(User).where(User.id == cv.user_id)
            user_result = await session.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if user:
                print(f"User Found: {user.full_name}")
                print(f"User Is Active: {user.is_active}")
                print(f"User Role: {user.role}")
            else:
                print("User NOT FOUND!")
            
            print("-" * 40)
        
        # Проверяем JOIN
        print("\n=== Проверка JOIN ===")
        join_stmt = (
            select(CV, User)
            .join(User)
            .where(CV.is_active == True, User.is_active == True)
        )
        
        join_result = await session.execute(join_stmt)
        joined_pairs = join_result.all()
        
        print(f"Активных CV с активными пользователями: {len(joined_pairs)}")
        
        for cv, user in joined_pairs:
            print(f"CV {cv.id} -> User {user.full_name} ({user.role})")


if __name__ == "__main__":
    asyncio.run(check_cvs())
