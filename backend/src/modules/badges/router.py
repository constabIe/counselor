from __future__ import annotations

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.badges import service as badge_service
from src.modules.badges.models import BadgeResponse, UserBadgesResponse, BadgeStatsResponse
from src.storages.sql.dependencies import get_db_session
from src.modules.users.dependencies import CurrentUserDep

router = APIRouter(
    prefix="/badges",
    tags=["badges"],
)


@router.get("/", response_model=List[BadgeResponse])
async def get_all_badges(
    session: AsyncSession = Depends(get_db_session)
) -> List[BadgeResponse]:
    """Получить все доступные бэйджи"""
    return await badge_service.badge_service.get_all_badges(session)


@router.get("/users/{user_id}", response_model=UserBadgesResponse)
async def get_user_badges(
    user_id: UUID,
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session)
) -> UserBadgesResponse:
    """Получить бэйджи конкретного пользователя"""
    # Проверяем права доступа - можно смотреть только свои бэйджи или у администратора
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра бэйджей этого пользователя"
        )
    
    return await badge_service.badge_service.get_user_badges(session, user_id)


@router.get("/users/{user_id}/stats", response_model=BadgeStatsResponse)
async def get_user_badge_stats(
    user_id: UUID,
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session)
) -> BadgeStatsResponse:
    """Получить статистику по бэйджам пользователя"""
    # Проверяем права доступа
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра статистики этого пользователя"
        )
    
    return await badge_service.badge_service.get_user_badge_stats(session, user_id)


@router.get("/my", response_model=UserBadgesResponse)
async def get_my_badges(
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session)
) -> UserBadgesResponse:
    """Получить свои бэйджи"""
    return await badge_service.badge_service.get_user_badges(session, current_user.id)


@router.get("/my/stats", response_model=BadgeStatsResponse) 
async def get_my_badge_stats(
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session)
) -> BadgeStatsResponse:
    """Получить статистику по своим бэйджам"""
    return await badge_service.badge_service.get_user_badge_stats(session, current_user.id)
