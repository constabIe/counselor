from __future__ import annotations

import logging
from typing import List, Optional, Any, Dict
from uuid import UUID
from datetime import datetime

from sqlmodel import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, text, and_

from src.storages.sql.models import CV

logger = logging.getLogger(__name__)


async def create_cv(
    session: AsyncSession,
    user_id: UUID,
    filename: str,
    original_filename: str,
    file_path: str,
    file_size: int,
    content_type: str,
    parsed_text: Optional[str] = None,
    skills: Optional[str] = None,
    experience_years: Optional[int] = None,
    education: Optional[str] = None,
    analysis_status: str = "pending",
) -> CV:
    """Создает новую запись CV в базе данных"""
    
    cv = CV(
        user_id=user_id,
        filename=filename,
        original_filename=original_filename,
        file_path=file_path,
        file_size=file_size,
        content_type=content_type,
        uploaded_at=datetime.utcnow(),
        is_active=True,
        parsed_text=parsed_text,
        skills=skills,
        experience_years=experience_years,
        education=education,
        analysis_status=analysis_status,
    )
    
    session.add(cv)
    await session.commit()
    await session.refresh(cv)
    
    logger.info(f"Создано CV с ID: {cv.id}")
    
    return cv


async def get_cv_by_id(
    session: AsyncSession,
    cv_id: UUID,
    include_inactive: bool = False
) -> Optional[CV]:
    """Получает CV по ID"""
    
    if include_inactive:
        stmt = select(CV).where(CV.id == cv_id)
    else:
        stmt = select(CV).where(CV.id == cv_id, CV.is_active == True)
    
    result = await session.execute(stmt)
    cv = result.scalar_one_or_none()
    
    return cv


async def get_user_cvs(
    session: AsyncSession,
    user_id: UUID,
    include_inactive: bool = False
) -> List[CV]:
    """Получает все CV пользователя"""
    
    if include_inactive:
        stmt = select(CV).where(CV.user_id == user_id)
    else:
        stmt = select(CV).where(CV.user_id == user_id, CV.is_active == True)
    
    stmt = stmt.order_by(text('uploaded_at DESC'))
    
    result = await session.execute(stmt)
    cvs = result.scalars().all()
    
    return list(cvs)


async def get_user_deleted_cvs(session: AsyncSession, user_id: UUID) -> List[CV]:
    """Получает все удаленные (неактивные) CV пользователя"""
    
    stmt = (
        select(CV)
        .where(CV.user_id == user_id, CV.is_active == False)
        .order_by(text('uploaded_at DESC'))
    )
    
    result = await session.execute(stmt)
    cvs = result.scalars().all()
    
    return list(cvs)


async def delete_cv(session: AsyncSession, cv_id: UUID, user_id: UUID) -> bool:
    """Мягкое удаление CV (устанавливает is_active = False)"""
    
    # Сначала проверяем, что CV существует и принадлежит пользователю
    stmt = select(CV).where(CV.id == cv_id, CV.user_id == user_id)
    result = await session.execute(stmt)
    cv = result.scalar_one_or_none()
    
    if not cv:
        return False
    
    # Обновляем запись напрямую
    cv.is_active = False
    session.add(cv)
    await session.commit()
    
    logger.info(f"CV с ID {cv_id} помечено как удаленное")
    
    return True


async def restore_cv(session: AsyncSession, cv_id: UUID) -> Optional[CV]:
    """Восстанавливает удаленное CV (устанавливает is_active = True)"""
    
    # Получаем CV (включая неактивные)
    stmt = select(CV).where(CV.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalar_one_or_none()
    
    if not cv:
        return None
    
    # Обновляем запись напрямую
    cv.is_active = True
    session.add(cv)
    await session.commit()
    await session.refresh(cv)
    
    logger.info(f"CV с ID {cv_id} восстановлено")
    
    return cv


async def update_cv_analysis(
    session: AsyncSession,
    cv_id: UUID,
    parsed_text: Optional[str] = None,
    skills: Optional[str] = None,
    experience_years: Optional[int] = None,
    education: Optional[str] = None,
    analysis_status: str = "completed",
) -> Optional[CV]:
    """Обновляет результаты анализа CV"""
    
    # Получаем CV
    stmt = select(CV).where(CV.id == cv_id)
    result = await session.execute(stmt)
    cv = result.scalar_one_or_none()
    
    if not cv:
        return None
    
    # Обновляем поля
    cv.analysis_status = analysis_status
    if parsed_text is not None:
        cv.parsed_text = parsed_text
    if skills is not None:
        cv.skills = skills
    if experience_years is not None:
        cv.experience_years = experience_years
    if education is not None:
        cv.education = education
    
    session.add(cv)
    await session.commit()
    await session.refresh(cv)
    
    logger.info(f"Анализ CV с ID {cv_id} обновлен")
    
    return cv


# async def hard_delete_cv(session: AsyncSession, cv_id: UUID, user_id: UUID) -> bool:
#     """Полное удаление CV из базы данных (использовать с осторожностью)"""
    
#     # Сначала проверяем, что CV существует и принадлежит пользователю
#     stmt = select(CV).where(CV.id == cv_id, CV.user_id == user_id)
#     result = await session.execute(stmt)
#     cv = result.scalar_one_or_none()
    
#     if not cv:
#         return False
    
#     # Удаляем CV из сессии
#     await session.delete(cv)
#     await session.commit()
    
#     logger.warning(f"CV с ID {cv_id} полностью удалено из базы данных")
    
#     return True
