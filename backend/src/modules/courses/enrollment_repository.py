from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from src.storages.sql.models import CourseEnrollment, Course, EnrollmentStatus

logger = logging.getLogger(__name__)


async def enroll_user_to_course(
    session: AsyncSession,
    user_id: UUID,
    course_id: UUID,
) -> CourseEnrollment:
    """Записывает пользователя на курс"""
    
    # Проверяем, что курс существует и активен
    course_stmt = select(Course).where(Course.id == course_id, Course.is_active == True)
    course_result = await session.execute(course_stmt)
    course = course_result.scalar_one_or_none()
    
    if not course:
        raise ValueError("Курс не найден или неактивен")
    
    # Проверяем, что пользователь еще не записан на этот курс
    existing_stmt = select(CourseEnrollment).where(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.is_active == True
    )
    existing_result = await session.execute(existing_stmt)
    existing_enrollment = existing_result.scalar_one_or_none()
    
    if existing_enrollment:
        raise ValueError("Пользователь уже записан на этот курс")
    
    # Создаем запись
    enrollment = CourseEnrollment(
        user_id=user_id,
        course_id=course_id,
        status=EnrollmentStatus.ENROLLED,
    )
    
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)
    
    logger.info(f"Пользователь {user_id} записан на курс {course_id}")
    
    return enrollment


async def get_user_enrollments(
    session: AsyncSession,
    user_id: UUID,
    status: Optional[EnrollmentStatus] = None,
) -> List[tuple[CourseEnrollment, Course]]:
    """Получает записи пользователя на курсы с информацией о курсах"""
    
    stmt = (
        select(CourseEnrollment, Course)
        .join(Course, CourseEnrollment.course_id == Course.id)
        .where(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.is_active == True,
            Course.is_active == True
        )
        .order_by(CourseEnrollment.enrolled_at.desc())
    )
    
    if status:
        stmt = stmt.where(CourseEnrollment.status == status)
    
    result = await session.execute(stmt)
    rows = result.all()
    return [(row[0], row[1]) for row in rows]


async def get_enrollment_by_id(
    session: AsyncSession,
    enrollment_id: UUID,
    user_id: Optional[UUID] = None,
) -> Optional[tuple[CourseEnrollment, Course]]:
    """Получает запись на курс по ID с информацией о курсе"""
    
    stmt = (
        select(CourseEnrollment, Course)
        .join(Course, CourseEnrollment.course_id == Course.id)
        .where(
            CourseEnrollment.id == enrollment_id,
            CourseEnrollment.is_active == True,
            Course.is_active == True
        )
    )
    
    if user_id:
        stmt = stmt.where(CourseEnrollment.user_id == user_id)
    
    result = await session.execute(stmt)
    row = result.first()
    return (row[0], row[1]) if row else None


async def update_enrollment_status(
    session: AsyncSession,
    enrollment_id: UUID,
    status: EnrollmentStatus,
    user_id: Optional[UUID] = None,
) -> Optional[CourseEnrollment]:
    """Обновляет статус записи на курс"""
    
    stmt = select(CourseEnrollment).where(
        CourseEnrollment.id == enrollment_id,
        CourseEnrollment.is_active == True
    )
    
    if user_id:
        stmt = stmt.where(CourseEnrollment.user_id == user_id)
    
    result = await session.execute(stmt)
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        return None
    
    enrollment.status = status
    
    # Если статус "начат", устанавливаем дату начала
    if status == EnrollmentStatus.STARTED and not enrollment.started_at:
        from src.storages.sql.models import utcnow
        enrollment.started_at = utcnow()
    
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)
    
    logger.info(f"Обновлен статус записи {enrollment_id} на {status}")
    
    return enrollment


async def count_user_enrollments(
    session: AsyncSession,
    user_id: UUID,
) -> int:
    """Подсчитывает количество активных записей пользователя на курсы"""
    
    stmt = select(func.count()).where(
        CourseEnrollment.user_id == user_id,
        CourseEnrollment.is_active == True
    )
    
    result = await session.execute(stmt)
    return result.scalar() or 0


async def get_enrollment_counts_by_status(
    session: AsyncSession,
    user_id: UUID,
) -> dict[str, int]:
    """Получает количество записей по статусам"""
    
    stmt = (
        select(CourseEnrollment.status, func.count())
        .where(
            CourseEnrollment.user_id == user_id,
            CourseEnrollment.is_active == True
        )
        .group_by(CourseEnrollment.status)
    )
    
    result = await session.execute(stmt)
    counts = {status: count for status, count in result.all()}
    
    # Заполняем нулями отсутствующие статусы
    return {
        "enrolled": counts.get(EnrollmentStatus.ENROLLED, 0),
        "started": counts.get(EnrollmentStatus.STARTED, 0),
        "completed": counts.get(EnrollmentStatus.COMPLETED, 0),
    }
