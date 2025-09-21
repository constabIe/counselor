from __future__ import annotations

import logging
import json
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlmodel import select, func, col
from sqlalchemy.ext.asyncio import AsyncSession

from src.storages.sql.models import Job, JobLevel, JobStatus, EmploymentType, Folder, FolderCandidate

logger = logging.getLogger(__name__)


async def create_job(
    session: AsyncSession,
    title: str,
    department: str,
    level: JobLevel,
    description: str,
    requirements: str,
    responsibilities: str,
    created_by: UUID,
    employment_type: EmploymentType = EmploymentType.FULL_TIME,
    location: Optional[str] = None,
    remote_available: bool = False,
    required_skills: Optional[list[str]] = None,
    min_experience_years: Optional[int] = None,
    max_experience_years: Optional[int] = None,
    average_salary: Optional[int] = None,
    salary_currency: str = "RUB",
) -> Job:
    """Создает новую вакансию"""
    
    job = Job(
        title=title,
        department=department,
        level=level,
        employment_type=employment_type,
        location=location,
        remote_available=remote_available,
        description=description,
        requirements=requirements,
        responsibilities=responsibilities,
        required_skills=json.dumps(required_skills, ensure_ascii=False) if required_skills else None,
        min_experience_years=min_experience_years,
        max_experience_years=max_experience_years,
        average_salary=average_salary,
        salary_currency=salary_currency,
        created_by=created_by,
    )
    
    session.add(job)
    await session.commit()
    await session.refresh(job)
    
    logger.info(f"Создана вакансия с ID: {job.id}, название: {job.title}")
    
    return job


async def get_job_by_id(
    session: AsyncSession,
    job_id: UUID,
) -> Optional[Job]:
    """Получает вакансию по ID"""
    
    stmt = select(Job).where(Job.id == job_id)
    result = await session.execute(stmt)
    job = result.scalar_one_or_none()
    
    return job


async def get_jobs(
    session: AsyncSession,
    page: int = 1,
    per_page: int = 10,
    status: Optional[JobStatus] = None,
    level: Optional[JobLevel] = None,
    department: Optional[str] = None,
    remote_available: Optional[bool] = None,
    employment_type: Optional[EmploymentType] = None,
) -> tuple[List[Job], int]:
    """Получает список вакансий с фильтрацией и пагинацией"""
    
    # Базовый запрос
    stmt = select(Job)
    count_stmt = select(func.count())
    
    # Применяем фильтры
    if status is not None:
        stmt = stmt.where(Job.status == status)
        count_stmt = count_stmt.where(Job.status == status)
    
    if level is not None:
        stmt = stmt.where(Job.level == level)
        count_stmt = count_stmt.where(Job.level == level)
    
    if department is not None:
        stmt = stmt.where(col(Job.department).ilike(f"%{department}%"))
        count_stmt = count_stmt.where(col(Job.department).ilike(f"%{department}%"))
    
    if remote_available is not None:
        stmt = stmt.where(Job.remote_available == remote_available)
        count_stmt = count_stmt.where(Job.remote_available == remote_available)
    
    if employment_type is not None:
        stmt = stmt.where(Job.employment_type == employment_type)
        count_stmt = count_stmt.where(Job.employment_type == employment_type)
    
    # Добавляем сортировку по дате создания (новые первыми)
    stmt = stmt.order_by(col(Job.created_at).desc())
    
    # Добавляем пагинацию
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    
    # Выполняем запросы
    result = await session.execute(stmt)
    jobs = result.scalars().all()
    
    count_result = await session.execute(count_stmt.select_from(Job))
    total = count_result.scalar() or 0
    
    return list(jobs), total


async def update_job(
    session: AsyncSession,
    job_id: UUID,
    **updates
) -> Optional[Job]:
    """Обновляет вакансию"""
    
    job = await get_job_by_id(session, job_id)
    if not job:
        return None
    
    # Обработка списка навыков
    if "required_skills" in updates and updates["required_skills"] is not None:
        updates["required_skills"] = json.dumps(updates["required_skills"], ensure_ascii=False)
    
    # Обновляем поля
    for field, value in updates.items():
        if hasattr(job, field) and value is not None:
            setattr(job, field, value)
    
    # Обновляем время изменения
    job.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(job)
    
    logger.info(f"Обновлена вакансия с ID: {job.id}")
    
    return job


async def delete_job(
    session: AsyncSession,
    job_id: UUID,
) -> bool:
    """Удаляет вакансию"""
    
    job = await get_job_by_id(session, job_id)
    if not job:
        return False
    
    # Сначала удаляем все связанные папки (включая неактивные)
    # Получаем все папки для данной вакансии (включая неактивные)
    folders_stmt = select(Folder).where(Folder.job_id == job_id)
    folders_result = await session.execute(folders_stmt)
    folders = list(folders_result.scalars().all())
    
    # Удаляем кандидатов из всех папок
    for folder in folders:
        candidates_stmt = select(FolderCandidate).where(FolderCandidate.folder_id == folder.id)
        candidates_result = await session.execute(candidates_stmt)
        candidates = list(candidates_result.scalars().all())
        
        for candidate in candidates:
            await session.delete(candidate)
    
    # Удаляем все папки
    for folder in folders:
        await session.delete(folder)
    
    # Удаляем саму вакансию
    await session.delete(job)
    await session.commit()
    
    logger.info(f"Удалена вакансия с ID: {job_id} и все связанные папки ({len(folders)} шт.)")
    
    return True


async def publish_job(
    session: AsyncSession,
    job_id: UUID,
) -> Optional[Job]:
    """Публикует вакансию (меняет статус на ACTIVE)"""
    
    job = await get_job_by_id(session, job_id)
    if not job:
        return None
    
    job.status = JobStatus.ACTIVE
    job.published_at = datetime.utcnow()
    job.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(job)
    
    logger.info(f"Опубликована вакансия с ID: {job.id}")
    
    return job


async def pause_job(
    session: AsyncSession,
    job_id: UUID,
) -> Optional[Job]:
    """Приостанавливает вакансию (меняет статус на PAUSED)"""
    
    job = await get_job_by_id(session, job_id)
    if not job:
        return None
    
    job.status = JobStatus.PAUSED
    job.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(job)
    
    logger.info(f"Приостановлена вакансия с ID: {job.id}")
    
    return job


async def close_job(
    session: AsyncSession,
    job_id: UUID,
) -> Optional[Job]:
    """Закрывает вакансию (меняет статус на CLOSED)"""
    
    job = await get_job_by_id(session, job_id)
    if not job:
        return None
    
    job.status = JobStatus.CLOSED
    job.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(job)
    
    logger.info(f"Закрыта вакансия с ID: {job.id}")
    
    return job


async def get_jobs_by_creator(
    session: AsyncSession,
    creator_id: UUID,
    page: int = 1,
    per_page: int = 10,
) -> tuple[List[Job], int]:
    """Получает вакансии, созданные определенным пользователем"""
    
    stmt = select(Job).where(Job.created_by == creator_id)
    count_stmt = select(func.count()).where(Job.created_by == creator_id)
    
    # Добавляем сортировку по дате создания (новые первыми)
    stmt = stmt.order_by(col(Job.created_at).desc())
    
    # Добавляем пагинацию
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    
    # Выполняем запросы
    result = await session.execute(stmt)
    jobs = result.scalars().all()
    
    count_result = await session.execute(count_stmt.select_from(Job))
    total = count_result.scalar() or 0
    
    return list(jobs), total
