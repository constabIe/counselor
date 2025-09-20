from __future__ import annotations

from typing import List, Optional, Set
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.storages.sql.models import Badge, UserBadge, User


async def get_all_badges(session: AsyncSession) -> List[Badge]:
    """Получает все бэйджи"""
    result = await session.execute(
        select(Badge).order_by(Badge.category, Badge.name)  # type: ignore
    )
    return list(result.scalars().all())


async def get_badge_by_code(session: AsyncSession, code: str) -> Optional[Badge]:
    """Получает бэйдж по коду"""
    result = await session.execute(select(Badge).where(Badge.code == code))  # type: ignore
    return result.scalar_one_or_none()


async def get_user_badges(session: AsyncSession, user_id: UUID) -> List[UserBadge]:
    """Получает все бэйджи пользователя"""
    result = await session.execute(
        select(UserBadge)
        .where(UserBadge.user_id == user_id)  # type: ignore
        .order_by(UserBadge.earned_at.desc())  # type: ignore
    )
    return list(result.scalars().all())


async def get_user_badge_codes(session: AsyncSession, user_id: UUID) -> Set[str]:
    """Получает коды всех бэйджей пользователя"""
    result = await session.execute(
        select(Badge.code)  # type: ignore
        .join(UserBadge)  # type: ignore
        .where(UserBadge.user_id == user_id)  # type: ignore
    )
    return set(result.scalars().all())


async def create_user_badge(session: AsyncSession, user_id: UUID, badge_id: UUID) -> UserBadge:
    """Создаёт связь пользователя с бэйджем"""
    user_badge = UserBadge(
        user_id=user_id,
        badge_id=badge_id
    )
    session.add(user_badge)
    await session.flush()
    await session.refresh(user_badge)
    return user_badge


async def user_has_badge(session: AsyncSession, user_id: UUID, badge_code: str) -> bool:
    """Проверяет, есть ли у пользователя бэйдж"""
    result = await session.execute(
        select(UserBadge)  # type: ignore
        .join(Badge)  # type: ignore
        .where(UserBadge.user_id == user_id, Badge.code == badge_code)  # type: ignore
    )
    return result.scalar_one_or_none() is not None


async def get_user_badge_stats(session: AsyncSession, user_id: UUID) -> dict:
    """Получает статистику по бэйджам пользователя"""
    # Общее количество бэйджей
    total_badges_result = await session.execute(
        select(func.count(Badge.id))  # type: ignore
    )
    total_badges = total_badges_result.scalar() or 0
    
    # Количество заработанных бэйджей
    earned_badges_result = await session.execute(
        select(func.count(UserBadge.id)).where(UserBadge.user_id == user_id)  # type: ignore
    )
    earned_badges = earned_badges_result.scalar() or 0
    
    # Общий XP от бэйджей
    total_xp_result = await session.execute(
        select(func.sum(Badge.xp_reward))  # type: ignore
        .join(UserBadge)  # type: ignore
        .where(UserBadge.user_id == user_id)  # type: ignore
    )
    total_xp = total_xp_result.scalar() or 0
    
    # Статистика по категориям
    category_stats_result = await session.execute(
        select(Badge.category, func.count(UserBadge.id))  # type: ignore
        .join(UserBadge)  # type: ignore
        .where(UserBadge.user_id == user_id)  # type: ignore
        .group_by(Badge.category)  # type: ignore
    )
    
    by_category = {}
    for category, count in category_stats_result.all():
        by_category[category.value] = count
    
    return {
        "earned_badges": earned_badges,
        "total_badges": total_badges,
        "completion_percentage": (earned_badges / total_badges * 100) if total_badges > 0 else 0,
        "total_xp_from_badges": total_xp,
        "by_category": by_category
    }


async def create_badge(session: AsyncSession, badge_data: dict) -> Badge:
    """Создаёт новый бэйдж"""
    badge = Badge(**badge_data)
    session.add(badge)
    await session.flush()
    await session.refresh(badge)
    return badge
