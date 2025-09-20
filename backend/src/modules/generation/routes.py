from __future__ import annotations

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends

from src.modules.generation.schemas import (
    GenerationRequest, 
    GenerationResponse,
    EmployeeBasic,
    GenerationFilters
)
from src.modules.generation.service import GenerationService
from src.modules.generation import repository as gen_repo
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/generation",
    tags=["Employee Generation"],
)

# Создаем экземпляр сервиса
generation_service = GenerationService()


@router.post(
    "/employees",
    response_model=GenerationResponse,
    summary="Генерация сотрудников",
    description="Генерирует список подходящих сотрудников на основе запроса HR и фильтров"
)
async def generate_employees(
    request: GenerationRequest,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> GenerationResponse:
    """Генерирует список сотрудников по запросу"""
    
    # Проверяем права доступа (только HR и админы могут использовать генерацию)
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для использования генерации сотрудников"
        )
    
    try:
        response = await generation_service.generate_employees(session, request)
        
        print(
            f"Пользователь {current_user.id} ({current_user.role}) "
            f"выполнил запрос генерации: '{request.query}', "
            f"найдено {response.total_found} сотрудников"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Ошибка при генерации сотрудников: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при генерации сотрудников"
        )


@router.get(
    "/employees/{cv_id}",
    response_model=EmployeeBasic,
    summary="Получить информацию о сотруднике",
    description="Получает базовую информацию о конкретном сотруднике по ID резюме"
)
async def get_employee_info(
    cv_id: UUID,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> EmployeeBasic:
    """Получает информацию о сотруднике по ID резюме"""
    
    # Проверяем права доступа
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра информации о сотрудниках"
        )
    
    employee = await gen_repo.get_employee_basic_info(session, cv_id)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сотрудник не найден"
        )
    
    return employee


@router.post(
    "/search",
    response_model=List[EmployeeBasic],
    summary="Поиск сотрудников по тегам",
    description="Прямой поиск сотрудников по списку тегов (для отладки)"
)
async def search_employees_by_tags(
    tags: List[str],
    current_user: CurrentUserDep,
    session: DbSessionDep,
    limit: int = 20
) -> List[EmployeeBasic]:
    """Поиск сотрудников по тегам (для отладки)"""
    
    # Проверяем права доступа
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для поиска сотрудников"
        )
    
    if not tags:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать хотя бы один тег"
        )
    
    empty_filters = GenerationFilters(
        department=None,
        experience_years_min=None,
        experience_years_max=None,
        skills=None,
        level=None,
        languages=None,
        education_level=None,
        age_min=None,
        age_max=None
    )
    
    employees = await gen_repo.search_employees_by_tags(
        session=session,
        tags=tags,
        filters=empty_filters,
        limit=limit
    )
    
    return employees