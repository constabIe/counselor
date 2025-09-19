from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.storages.sql.models import User
from src.utils.security import hash_password


async def create_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str,
) -> User:
    """Создает нового пользователя"""
    password_hash = hash_password(password)
    
    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
    )
    
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Получает пользователя по email"""
    result = await session.execute(select(User).where(User.email == email)) # type: ignore
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
    """Получает пользователя по ID"""
    result = await session.execute(select(User).where(User.id == user_id)) # type: ignore
    return result.scalar_one_or_none()


async def update_user(
    session: AsyncSession,
    user: User,
    **kwargs
) -> User:
    """Обновляет данные пользователя"""
    for field, value in kwargs.items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    await session.flush()
    await session.refresh(user)
    return user
