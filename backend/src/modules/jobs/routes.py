from __future__ import annotations

import logging
import json
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query

from src.modules.jobs import repository as jobs_repo
from src.modules.jobs.schemas import JobOut, JobCreate, JobUpdate, JobList
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep
from src.storages.sql.models import JobLevel, JobStatus, EmploymentType

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


def _parse_skills(skills_json: Optional[str]) -> Optional[List[str]]:
    """Парсит JSON строку с навыками в список"""
    if not skills_json:
        return None
    try:
        return json.loads(skills_json)
    except (json.JSONDecodeError, TypeError):
        return None


def _job_to_schema(job) -> JobOut:
    """Конвертирует модель Job в схему JobOut"""
    return JobOut(
        id=job.id,
        title=job.title,
        department=job.department,
        level=job.level,
        employment_type=job.employment_type,
        location=job.location,
        remote_available=job.remote_available,
        description=job.description,
        requirements=job.requirements,
        responsibilities=job.responsibilities,
        required_skills=_parse_skills(job.required_skills),
        min_experience_years=job.min_experience_years,
        max_experience_years=job.max_experience_years,
        average_salary=job.average_salary,
        salary_currency=job.salary_currency,
        status=job.status,
        created_by=job.created_by,
        created_at=job.created_at,
        updated_at=job.updated_at,
        published_at=job.published_at,
    )


@router.get(
    "/",
    response_model=JobList,
    summary="Получить все вакансии",
    description="Получает список всех вакансий с возможностью фильтрации и пагинации"
)
async def get_jobs(
    session: DbSessionDep,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
    status: Optional[JobStatus] = Query(None, description="Фильтр по статусу"),
    level: Optional[JobLevel] = Query(None, description="Фильтр по уровню"),
    department: Optional[str] = Query(None, description="Фильтр по отделу"),
    remote_available: Optional[bool] = Query(None, description="Фильтр по удаленной работе"),
    employment_type: Optional[EmploymentType] = Query(None, description="Фильтр по типу занятости"),
) -> JobList:
    """Получает все вакансии с фильтрацией"""
    
    jobs, total = await jobs_repo.get_jobs(
        session=session,
        page=page,
        per_page=per_page,
        status=status,
        level=level,
        department=department,
        remote_available=remote_available,
        employment_type=employment_type,
    )
    
    return JobList(
        jobs=[_job_to_schema(job) for job in jobs],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{job_id}",
    response_model=JobOut,
    summary="Получить вакансию",
    description="Получает вакансию по её ID"
)
async def get_job(
    session: DbSessionDep,
    job_id: UUID,
) -> JobOut:
    """Получает вакансию по ID"""
    
    job = await jobs_repo.get_job_by_id(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    return _job_to_schema(job)


@router.post(
    "/",
    response_model=JobOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать вакансию",
    description="Создает новую вакансию"
)
async def create_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_data: JobCreate,
) -> JobOut:
    """Создает новую вакансию"""
    
    # Проверяем права пользователя (только HR и ADMIN могут создавать вакансии)
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для создания вакансий"
        )
    
    job = await jobs_repo.create_job(
        session=session,
        title=job_data.title,
        department=job_data.department,
        level=job_data.level,
        description=job_data.description,
        requirements=job_data.requirements,
        responsibilities=job_data.responsibilities,
        created_by=current_user.id,
        employment_type=job_data.employment_type,
        location=job_data.location,
        remote_available=job_data.remote_available,
        required_skills=job_data.required_skills,
        min_experience_years=job_data.min_experience_years,
        max_experience_years=job_data.max_experience_years,
        average_salary=job_data.average_salary,
        salary_currency=job_data.salary_currency,
    )
    
    return _job_to_schema(job)


@router.put(
    "/{job_id}",
    response_model=JobOut,
    summary="Обновить вакансию",
    description="Обновляет существующую вакансию"
)
async def update_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_id: UUID,
    job_data: JobUpdate,
) -> JobOut:
    """Обновляет вакансию"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для обновления вакансий"
        )
    
    # Получаем вакансию
    existing_job = await jobs_repo.get_job_by_id(session, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    # Проверяем, что пользователь может редактировать эту вакансию
    if current_user.role != "admin" and existing_job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно редактировать только свои вакансии"
        )
    
    # Подготавливаем данные для обновления
    update_data = {}
    for field, value in job_data.model_dump(exclude_unset=True).items():
        if value is not None:
            update_data[field] = value
    
    if not update_data:
        return _job_to_schema(existing_job)
    
    job = await jobs_repo.update_job(session, job_id, **update_data)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    return _job_to_schema(job)


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить вакансию",
    description="Удаляет вакансию"
)
async def delete_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_id: UUID,
):
    """Удаляет вакансию"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления вакансий"
        )
    
    # Получаем вакансию
    existing_job = await jobs_repo.get_job_by_id(session, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    # Проверяем, что пользователь может удалить эту вакансию
    if current_user.role != "admin" and existing_job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно удалять только свои вакансии"
        )
    
    success = await jobs_repo.delete_job(session, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )


@router.post(
    "/{job_id}/publish",
    response_model=JobOut,
    summary="Опубликовать вакансию",
    description="Публикует вакансию (меняет статус на ACTIVE)"
)
async def publish_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_id: UUID,
) -> JobOut:
    """Публикует вакансию"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для публикации вакансий"
        )
    
    # Получаем вакансию
    existing_job = await jobs_repo.get_job_by_id(session, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    # Проверяем, что пользователь может публиковать эту вакансию
    if current_user.role != "admin" and existing_job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно публиковать только свои вакансии"
        )
    
    job = await jobs_repo.publish_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    return _job_to_schema(job)


@router.post(
    "/{job_id}/pause",
    response_model=JobOut,
    summary="Приостановить вакансию",
    description="Приостанавливает вакансию (меняет статус на PAUSED)"
)
async def pause_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_id: UUID,
) -> JobOut:
    """Приостанавливает вакансию"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для управления вакансиями"
        )
    
    # Получаем вакансию
    existing_job = await jobs_repo.get_job_by_id(session, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    # Проверяем, что пользователь может управлять этой вакансией
    if current_user.role != "admin" and existing_job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно управлять только своими вакансиями"
        )
    
    job = await jobs_repo.pause_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    return _job_to_schema(job)


@router.post(
    "/{job_id}/close",
    response_model=JobOut,
    summary="Закрыть вакансию",
    description="Закрывает вакансию (меняет статус на CLOSED)"
)
async def close_job(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    job_id: UUID,
) -> JobOut:
    """Закрывает вакансию"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для управления вакансиями"
        )
    
    # Получаем вакансию
    existing_job = await jobs_repo.get_job_by_id(session, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    # Проверяем, что пользователь может управлять этой вакансией
    if current_user.role != "admin" and existing_job.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно управлять только своими вакансиями"
        )
    
    job = await jobs_repo.close_job(session, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вакансия не найдена"
        )
    
    return _job_to_schema(job)


@router.get(
    "/my/jobs",
    response_model=JobList,
    summary="Получить мои вакансии",
    description="Получает вакансии, созданные текущим пользователем"
)
async def get_my_jobs(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
) -> JobList:
    """Получает вакансии текущего пользователя"""
    
    # Проверяем права пользователя
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра вакансий"
        )
    
    jobs, total = await jobs_repo.get_jobs_by_creator(
        session=session,
        creator_id=current_user.id,
        page=page,
        per_page=per_page,
    )
    
    return JobList(
        jobs=[_job_to_schema(job) for job in jobs],
        total=total,
        page=page,
        per_page=per_page,
    )
