from __future__ import annotations

import logging
import json
from typing import List, Optional
from uuid import UUID

from sqlmodel import select, text, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.storages.sql.models import CV, User
from src.modules.generation.schemas import EmployeeBasic, GenerationFilters

logger = logging.getLogger(__name__)


async def search_employees_by_tags(
    session: AsyncSession,
    tags: List[str],
    filters: GenerationFilters,
    limit: int = 50
) -> List[EmployeeBasic]:
    """Ищет сотрудников по тегам и фильтрам"""
    
    # Базовый запрос для активных CV с пользователями
    stmt = (
        select(CV, User)
        .join(User, CV.user_id == User.id)
        .where(CV.is_active == True, User.is_active == True)
    )
    
    # Фильтр по тегам - ищем CV, у которых есть хотя бы один из указанных тегов
    if tags:
        tag_conditions = []
        for tag in tags:
            # Ищем теги в JSON поле tags
            tag_conditions.append(CV.tags.like(f'%"{tag}"%'))
            # Также ищем в навыках
            tag_conditions.append(CV.skills.like(f'%"{tag}"%')) # pyright: ignore[reportAttributeAccessIssue]
            # И в специализации
            tag_conditions.append(CV.specialization.like(f'%{tag}%'))
        
        stmt = stmt.where(or_(*tag_conditions))
    
    # Применяем фильтры
    if filters.department:
        stmt = stmt.where(CV.department == filters.department)
    
    if filters.experience_years_min is not None:
        stmt = stmt.where(CV.experience_years >= filters.experience_years_min)
    
    if filters.experience_years_max is not None:
        stmt = stmt.where(CV.experience_years <= filters.experience_years_max)
    
    if filters.age_min is not None:
        stmt = stmt.where(CV.age >= filters.age_min)
    
    if filters.age_max is not None:
        stmt = stmt.where(CV.age <= filters.age_max)
    
    # Фильтр по навыкам
    if filters.skills:
        skill_conditions = []
        for skill in filters.skills:
            skill_conditions.append(CV.skills.like(f'%"{skill}"%'))
        stmt = stmt.where(and_(*skill_conditions))
    
    # Фильтр по языкам
    if filters.languages:
        lang_conditions = []
        for lang in filters.languages:
            lang_conditions.append(CV.languages.like(f'%"{lang}"%'))
        stmt = stmt.where(and_(*lang_conditions))
    
    # Сортируем по рейтингу
    stmt = stmt.order_by(CV.rating.desc().nulls_last(), CV.experience_years.desc().nulls_last())
    
    # Ограничиваем количество результатов
    stmt = stmt.limit(limit)
    
    result = await session.execute(stmt)
    cv_user_pairs = result.all()
    
    employees = []
    for cv, user in cv_user_pairs:
        # Извлекаем навыки из JSON
        skills = []
        if cv.skills:
            try:
                skills_data = json.loads(cv.skills)
                if isinstance(skills_data, list):
                    skills = skills_data[:5]  # Берем первые 5 навыков
                elif isinstance(skills_data, dict) and 'skills' in skills_data:
                    skills = skills_data['skills'][:5]
            except json.JSONDecodeError:
                skills = []
        
        # Вычисляем match_score на основе соответствия тегам
        match_score = _calculate_match_score(cv, tags)
        
        employee = EmployeeBasic(
            id=cv.id,
            name=user.full_name,
            department=cv.department,
            experience_years=cv.experience_years,
            rating=cv.rating,
            skills=skills,
            match_score=match_score
        )
        employees.append(employee)
    
    logger.info(f"Найдено {len(employees)} сотрудников по тегам: {tags}")
    
    return employees


def _calculate_match_score(cv: CV, tags: List[str]) -> float:
    """Вычисляет степень соответствия CV тегам"""
    
    if not tags:
        return 0.0
    
    matches = 0
    total_tags = len(tags)
    
    # Проверяем соответствие в различных полях CV
    cv_text = ""
    
    if cv.tags:
        cv_text += cv.tags.lower()
    if cv.skills:
        cv_text += " " + cv.skills.lower()
    if cv.specialization:
        cv_text += " " + cv.specialization.lower()
    if cv.competencies:
        cv_text += " " + cv.competencies.lower()
    
    for tag in tags:
        if tag.lower() in cv_text:
            matches += 1
    
    # Бонус за высокий рейтинг
    rating_bonus = 0.0
    if cv.rating:
        rating_bonus = min(0.2, cv.rating / 50)  # До 20% бонуса за рейтинг
    
    base_score = matches / total_tags
    final_score = min(1.0, base_score + rating_bonus)
    
    return round(final_score, 2)


async def get_employee_basic_info(session: AsyncSession, cv_id: UUID) -> Optional[EmployeeBasic]:
    """Получает базовую информацию о сотруднике по ID CV"""
    
    logger.debug(f"Поиск сотрудника по CV ID: {cv_id}")
    
    # Сначала проверим, существует ли CV с данным ID
    cv_check_stmt = select(CV).where(CV.id == cv_id)
    cv_check_result = await session.execute(cv_check_stmt)
    cv_exists = cv_check_result.first()
    
    if not cv_exists:
        logger.debug(f"CV с ID {cv_id} не найдено")
        return None
    
    logger.debug(f"CV найдено: id={cv_exists[0].id}, user_id={cv_exists[0].user_id}, is_active={cv_exists[0].is_active}")
    
    # Проверим пользователя
    user_check_stmt = select(User).where(User.id == cv_exists[0].user_id)
    user_check_result = await session.execute(user_check_stmt)
    user_exists = user_check_result.first()
    
    if user_exists:
        logger.debug(f"Пользователь найден: id={user_exists[0].id}, is_active={user_exists[0].is_active}")
    else:
        logger.debug(f"Пользователь с ID {cv_exists[0].user_id} не найден")
    
    stmt = (
        select(CV, User)
        .join(User, CV.user_id == User.id) # pyright: ignore[reportArgumentType]
        .where(CV.id == cv_id, CV.is_active == True, User.is_active == True)
    )
    
    result = await session.execute(stmt)
    cv_user_pair = result.first()
    
    logger.debug(f"Результат JOIN запроса: {cv_user_pair}")
    
    if not cv_user_pair:
        logger.debug(f"JOIN не вернул результатов для CV ID {cv_id}")
        return None
    
    cv, user = cv_user_pair
    
    logger.debug(f"Найден сотрудник: CV ID={cv.id}, User ID={user.id}, Name={user.full_name}")
    
    # Извлекаем навыки
    skills = []
    if cv.skills:
        try:
            skills_data = json.loads(cv.skills)
            if isinstance(skills_data, list):
                skills = skills_data[:5]
            elif isinstance(skills_data, dict) and 'skills' in skills_data:
                skills = skills_data['skills'][:5]
        except json.JSONDecodeError:
            logger.warning(f"Ошибка парсинга skills для CV {cv.id}: {cv.skills}")
            skills = []
    
    return EmployeeBasic(
        id=cv.id,
        name=user.full_name,
        department=cv.department,
        experience_years=cv.experience_years,
        rating=cv.rating,
        skills=skills,
        match_score=1.0  # Для одиночного результата
    )