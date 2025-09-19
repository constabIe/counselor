from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storages.sql.models import Course, CourseLevel

logger = logging.getLogger(__name__)


async def create_course(
    session: AsyncSession,
    title: str,
    direction: str,
    level: CourseLevel,
    duration_hours: int,
    description: Optional[str] = None,
) -> Course:
    """Создает новый курс"""
    
    course = Course(
        title=title,
        direction=direction,
        level=level,
        duration_hours=duration_hours,
        description=description,
    )
    
    session.add(course)
    await session.commit()
    await session.refresh(course)
    
    logger.info(f"Создан курс с ID: {course.id}, название: {course.title}")
    
    return course


async def get_course_by_id(
    session: AsyncSession,
    course_id: UUID,
    include_inactive: bool = False
) -> Optional[Course]:
    """Получает курс по ID"""
    
    if include_inactive:
        stmt = select(Course).where(Course.id == course_id)
    else:
        stmt = select(Course).where(Course.id == course_id, Course.is_active == True)
    
    result = await session.execute(stmt)
    course = result.scalar_one_or_none()
    
    return course


async def get_all_courses(
    session: AsyncSession,
    direction: Optional[str] = None,
    level: Optional[CourseLevel] = None,
    include_inactive: bool = False
) -> List[Course]:
    """Получает все курсы с возможностью фильтрации"""
    
    stmt = select(Course)
    
    if not include_inactive:
        stmt = stmt.where(Course.is_active == True)
    
    if direction:
        stmt = stmt.where(Course.direction == direction)
    
    if level:
        stmt = stmt.where(Course.level == level)
    
    stmt = stmt.order_by(Course.direction, Course.level, Course.title)
    
    result = await session.execute(stmt)
    courses = result.scalars().all()
    
    return list(courses)


async def update_course(
    session: AsyncSession,
    course_id: UUID,
    **fields_to_update
) -> Optional[Course]:
    """Обновляет поля курса"""
    
    # Получаем курс
    stmt = select(Course).where(Course.id == course_id, Course.is_active == True)
    result = await session.execute(stmt)
    course = result.scalar_one_or_none()
    
    if not course:
        return None
    
    # Обновляем только переданные поля
    updated = False
    for field_name, field_value in fields_to_update.items():
        if hasattr(course, field_name) and field_value is not None:
            setattr(course, field_name, field_value)
            updated = True
    
    if updated:
        session.add(course)
        await session.commit()
        await session.refresh(course)
        
        logger.info(f"Курс с ID {course_id} обновлен")
    
    return course


async def delete_course(session: AsyncSession, course_id: UUID) -> bool:
    """Мягкое удаление курса (устанавливает is_active = False)"""
    
    # Получаем курс
    stmt = select(Course).where(Course.id == course_id, Course.is_active == True)
    result = await session.execute(stmt)
    course = result.scalar_one_or_none()
    
    if not course:
        return False
    
    # Обновляем запись
    course.is_active = False
    session.add(course)
    await session.commit()
    
    logger.info(f"Курс с ID {course_id} помечен как удаленный")
    
    return True


async def get_courses_by_direction(
    session: AsyncSession,
    direction: str,
    include_inactive: bool = False
) -> List[Course]:
    """Получает курсы по направлению"""
    
    stmt = select(Course).where(Course.direction == direction)
    
    if not include_inactive:
        stmt = stmt.where(Course.is_active == True)
    
    stmt = stmt.order_by(Course.level, Course.title)
    
    result = await session.execute(stmt)
    courses = result.scalars().all()
    
    return list(courses)
