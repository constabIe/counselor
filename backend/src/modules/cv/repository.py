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


async def get_user_active_cv_count(session: AsyncSession, user_id: UUID) -> int:
    """Возвращает количество активных CV пользователя"""
    
    stmt = select(CV).where(CV.user_id == user_id, CV.is_active == True)
    result = await session.execute(stmt)
    active_cvs = result.scalars().all()
    
    return len(active_cvs)


async def deactivate_user_cvs(session: AsyncSession, user_id: UUID) -> int:
    """Деактивирует все активные CV пользователя и возвращает количество деактивированных"""
    
    # Получаем все активные CV пользователя
    stmt = select(CV).where(CV.user_id == user_id, CV.is_active == True)
    result = await session.execute(stmt)
    active_cvs = result.scalars().all()
    
    # Деактивируем их
    deactivated_count = 0
    for cv in active_cvs:
        cv.is_active = False
        session.add(cv)
        deactivated_count += 1
    
    if deactivated_count > 0:
        await session.commit()
        logger.info(f"Деактивировано {deactivated_count} CV для пользователя {user_id}")
    
    return deactivated_count


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
    additional_education: Optional[str] = None,
    jobs: Optional[str] = None,
    current_role: Optional[str] = None,
    responsibilities: Optional[str] = None,
    languages: Optional[str] = None,
    age: Optional[int] = None,
    department: Optional[str] = None,
    grade: Optional[str] = None,
    specialization: Optional[str] = None,
    competencies: Optional[str] = None,
    comments: Optional[str] = None,
    rating: Optional[float] = None,
    tags: Optional[str] = None,
    career_path: Optional[str] = None,
    analysis_status: str = "pending",
) -> CV:
    """Создает новую запись CV в базе данных"""
    
    # Сначала деактивируем все предыдущие активные CV пользователя
    deactivated_count = await deactivate_user_cvs(session, user_id)
    if deactivated_count > 0:
        logger.info(f"Деактивировано {deactivated_count} старых CV при создании нового")
    
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
        additional_education=additional_education,
        jobs=jobs,
        current_role=current_role,
        responsibilities=responsibilities,
        languages=languages,
        age=age,
        department=department,
        grade=grade,
        specialization=specialization,
        competencies=competencies,
        comments=comments,
        rating=rating,
        tags=tags,
        career_path=career_path,
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
    additional_education: Optional[str] = None,
    jobs: Optional[str] = None,
    current_role: Optional[str] = None,
    responsibilities: Optional[str] = None,
    languages: Optional[str] = None,
    age: Optional[int] = None,
    department: Optional[str] = None,
    grade: Optional[str] = None,
    specialization: Optional[str] = None,
    competencies: Optional[str] = None,
    comments: Optional[str] = None,
    rating: Optional[float] = None,
    tags: Optional[str] = None,
    career_path: Optional[str] = None,
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
    if additional_education is not None:
        cv.additional_education = additional_education
    if jobs is not None:
        cv.jobs = jobs
    if current_role is not None:
        cv.current_role = current_role
    if responsibilities is not None:
        cv.responsibilities = responsibilities
    if languages is not None:
        cv.languages = languages
    if age is not None:
        cv.age = age
    if department is not None:
        cv.department = department
    if grade is not None:
        cv.grade = grade
    if specialization is not None:
        cv.specialization = specialization
    if competencies is not None:
        cv.competencies = competencies
    if comments is not None:
        cv.comments = comments
    if rating is not None:
        cv.rating = rating
    if tags is not None:
        cv.tags = tags
    if career_path is not None:
        cv.career_path = career_path
    
    session.add(cv)
    await session.commit()
    await session.refresh(cv)
    
    logger.info(f"Анализ CV с ID {cv_id} обновлен")
    
    return cv


async def update_cv_fields(
    session: AsyncSession,
    cv_id: UUID,
    user_id: UUID,
    **fields_to_update
) -> Optional[CV]:
    """Обновляет поля CV и пересчитывает рейтинг"""
    
    # Получаем CV и проверяем права доступа
    stmt = select(CV).where(CV.id == cv_id, CV.user_id == user_id, CV.is_active == True)
    result = await session.execute(stmt)
    cv = result.scalar_one_or_none()
    
    if not cv:
        return None
    
    # Обновляем только переданные поля
    updated = False
    for field_name, field_value in fields_to_update.items():
        if hasattr(cv, field_name) and field_value is not None:
            setattr(cv, field_name, field_value)
            updated = True
    
    if updated:
        # Пересчитываем рейтинг на основе обновленных данных
        cv.rating = _calculate_rating(cv)
        
        session.add(cv)
        await session.commit()
        await session.refresh(cv)
        
        logger.info(f"CV с ID {cv_id} обновлено пользователем {user_id}")
    
    return cv


'''TODO: Нужно переписать эту функцию и обсудить логику рейтинга'''
def _calculate_rating(cv: CV) -> float:
    """Функция для расчета рейтинга CV на основе заполненных полей"""
    
    score = 0.0
    max_score = 0.0
    
    # Проверяем наличие навыков (вес: 2.5)
    if cv.skills:
        try:
            import json
            skills_list = json.loads(cv.skills) if isinstance(cv.skills, str) else cv.skills
            if skills_list and len(skills_list) > 0:
                score += min(2.5, len(skills_list) * 0.25)
        except:
            score += 1.0
    max_score += 2.5
    
    # Проверяем опыт работы (вес: 2.0)
    if cv.experience_years is not None:
        if cv.experience_years >= 5:
            score += 2.0
        elif cv.experience_years >= 2:
            score += 1.5
        elif cv.experience_years >= 0:
            score += 0.8
    max_score += 2.0
    
    # Проверяем образование (вес: 1.5)
    if cv.education:
        score += 1.5
    max_score += 1.5
    
    # Проверяем дополнительное образование (вес: 1.0)
    if cv.additional_education:
        score += 1.0
    max_score += 1.0
    
    # Проверяем историю работы (вес: 1.5)
    if cv.jobs:
        try:
            import json
            jobs_list = json.loads(cv.jobs) if isinstance(cv.jobs, str) else cv.jobs
            if jobs_list and len(jobs_list) > 0:
                score += min(1.5, len(jobs_list) * 0.5)
        except:
            score += 0.5
    max_score += 1.5
    
    # Проверяем текущую роль (вес: 1.0)
    if cv.current_role:
        score += 1.0
    max_score += 1.0
    
    # Проверяем компетенции (вес: 1.5)
    if cv.competencies:
        try:
            import json
            competencies_data = json.loads(cv.competencies) if isinstance(cv.competencies, str) else cv.competencies
            if competencies_data:
                score += 1.5
        except:
            score += 0.5
    max_score += 1.5
    
    # Проверяем языки (вес: 0.8)
    if cv.languages:
        try:
            import json
            languages_list = json.loads(cv.languages) if isinstance(cv.languages, str) else cv.languages
            if languages_list and len(languages_list) > 0:
                score += min(0.8, len(languages_list) * 0.2)
        except:
            score += 0.3
    max_score += 0.8
    
    # Проверяем специализацию (вес: 0.7)
    if cv.specialization:
        score += 0.7
    max_score += 0.7
    
    # Нормализуем рейтинг к шкале 0-10
    if max_score > 0:
        normalized_score = (score / max_score) * 10
        return round(normalized_score, 2)
    
    return 0.0


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
