from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.storages.sql.models import User, UserRole, CV
from src.utils.security import hash_password


async def create_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str,
    role: UserRole = UserRole.USER,
) -> User:
    """Создает нового пользователя"""
    password_hash = hash_password(password)

    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role=role,
    )

    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Получает пользователя по email"""
    result = await session.execute(select(User).where(User.email == email))  # type: ignore
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> Optional[User]:
    """Получает пользователя по ID"""
    result = await session.execute(select(User).where(User.id == user_id))  # type: ignore
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


async def get_user_rating_percentile(session: AsyncSession, user_id: UUID) -> Optional[float]:
    """
    Возвращает процентиль рейтинга пользователя (на сколько процентов он лучше других).
    Возвращает None, если у пользователя нет активного CV с рейтингом.
    """
    # Получаем все активные CV с рейтингом
    all_cvs_stmt = select(CV).where(CV.is_active == True) # type: ignore
    all_cvs_result = await session.execute(all_cvs_stmt)
    all_cvs = all_cvs_result.scalars().all()

    # Фильтруем CV с рейтингом и находим рейтинг текущего пользователя
    current_user_rating = None
    user_ratings = {}

    for cv in all_cvs:
        if cv.rating is not None:
            # Для каждого пользователя берем максимальный рейтинг
            if cv.user_id not in user_ratings or cv.rating > user_ratings[cv.user_id]:
                user_ratings[cv.user_id] = cv.rating

            # Запоминаем рейтинг текущего пользователя
            if cv.user_id == user_id:
                if current_user_rating is None or cv.rating > current_user_rating:
                    current_user_rating = cv.rating

    if current_user_rating is None:
        return None

    if len(user_ratings) <= 1:
        return 100.0  # Если пользователь единственный с рейтингом

    # Считаем сколько пользователей имеют рейтинг ниже текущего
    lower_count = sum(1 for rating in user_ratings.values()
                      if rating < current_user_rating)

    # Вычисляем процентиль
    percentile = (lower_count / (len(user_ratings) - 1)) * 100
    return round(percentile, 1)
