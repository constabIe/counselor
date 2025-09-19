from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query

from src.modules.folders import repository as folders_repo
from src.modules.folders.schemas import (
    FolderOut, FolderCreate, FolderUpdate, FolderList,
    CandidateAddToFolder, CandidateUpdateInFolder,
    FolderCandidateOut, FolderCandidatesList
)
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/folders",
    tags=["Folders"],
)


async def _folder_to_schema(session, folder) -> FolderOut:
    """Конвертирует модель Folder в схему FolderOut"""
    candidates_count = await folders_repo.get_candidates_count_in_folder(session, folder.id)
    
    return FolderOut(
        id=folder.id,
        name=folder.name,
        description=folder.description,
        job_id=folder.job_id,
        created_by=folder.created_by,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
        is_active=folder.is_active,
        candidates_count=candidates_count,
    )


def _folder_candidate_to_schema(candidate) -> FolderCandidateOut:
    """Конвертирует модель FolderCandidate в схему FolderCandidateOut"""
    return FolderCandidateOut(
        id=candidate.id,
        folder_id=candidate.folder_id,
        user_id=candidate.user_id,
        user_full_name=getattr(candidate, 'user_full_name', ''),
        user_email=getattr(candidate, 'user_email', ''),
        added_by=candidate.added_by,
        added_at=candidate.added_at,
        notes=candidate.notes,
        is_active=candidate.is_active,
    )


@router.post(
    "/",
    response_model=FolderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать папку",
    description="Создает новую папку для кандидатов"
)
async def create_folder(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_data: FolderCreate,
) -> FolderOut:
    """Создает новую папку"""
    folder = await folders_repo.create_folder(
        session=session,
        name=folder_data.name,
        description=folder_data.description,
        job_id=folder_data.job_id,
        created_by=current_user.id,
    )
    
    return await _folder_to_schema(session, folder)


@router.get(
    "/job/{job_id}",
    response_model=FolderList,
    summary="Получить папки для вакансии",
    description="Получает все папки для конкретной вакансии"
)
async def get_folders_by_job(
    session: DbSessionDep,
    job_id: UUID,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
) -> FolderList:
    """Получает папки для конкретной вакансии"""
    
    folders, total = await folders_repo.get_folders_by_job(
        session=session,
        job_id=job_id,
        page=page,
        per_page=per_page,
    )
    
    folder_schemas = []
    for folder in folders:
        folder_schema = await _folder_to_schema(session, folder)
        folder_schemas.append(folder_schema)
    
    return FolderList(
        folders=folder_schemas,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/my",
    response_model=FolderList,
    summary="Получить мои папки",
    description="Получает папки, созданные текущим пользователем"
)
async def get_my_folders(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
) -> FolderList:
    """Получает папки, созданные текущим пользователем"""
    
    folders, total = await folders_repo.get_folders_by_creator(
        session=session,
        creator_id=current_user.id,
        page=page,
        per_page=per_page,
    )
    
    folder_schemas = []
    for folder in folders:
        folder_schema = await _folder_to_schema(session, folder)
        folder_schemas.append(folder_schema)
    
    return FolderList(
        folders=folder_schemas,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{folder_id}",
    response_model=FolderOut,
    summary="Получить папку",
    description="Получает папку по её ID"
)
async def get_folder(
    session: DbSessionDep,
    folder_id: UUID,
) -> FolderOut:
    """Получает папку по ID"""
    
    folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    return await _folder_to_schema(session, folder)


@router.put(
    "/{folder_id}",
    response_model=FolderOut,
    summary="Обновить папку",
    description="Обновляет существующую папку"
)
async def update_folder(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_id: UUID,
    folder_data: FolderUpdate,
) -> FolderOut:
    """Обновляет папку"""
    
    # Проверяем, что папка существует
    existing_folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not existing_folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    # Проверяем права доступа (только создатель может редактировать)
    if existing_folder.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для редактирования папки"
        )
    
    folder = await folders_repo.update_folder(
        session=session,
        folder_id=folder_id,
        name=folder_data.name,
        description=folder_data.description,
    )
    
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    return await _folder_to_schema(session, folder)


@router.delete(
    "/{folder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить папку",
    description="Удаляет папку"
)
async def delete_folder(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_id: UUID,
):
    """Удаляет папку"""
    
    # Проверяем, что папка существует
    existing_folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not existing_folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    # Проверяем права доступа (только создатель может удалять)
    if existing_folder.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления папки"
        )
    
    success = await folders_repo.delete_folder(session, folder_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )


# Маршруты для работы с кандидатами в папках

@router.post(
    "/{folder_id}/candidates",
    response_model=FolderCandidateOut,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить кандидата в папку",
    description="Добавляет кандидата в папку"
)
async def add_candidate_to_folder(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_id: UUID,
    candidate_data: CandidateAddToFolder,
) -> FolderCandidateOut:
    """Добавляет кандидата в папку"""
    
    # Проверяем, что папка существует
    folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    # Проверяем права доступа (только создатель папки может добавлять кандидатов)
    if folder.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для добавления кандидатов в папку"
        )
    
    folder_candidate = await folders_repo.add_candidate_to_folder(
        session=session,
        folder_id=folder_id,
        user_id=candidate_data.user_id,
        added_by=current_user.id,
        notes=candidate_data.notes,
    )
    
    if not folder_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Кандидат уже добавлен в папку или не найден"
        )
    
    return _folder_candidate_to_schema(folder_candidate)


@router.get(
    "/{folder_id}/candidates",
    response_model=FolderCandidatesList,
    summary="Получить кандидатов из папки",
    description="Получает список кандидатов в папке"
)
async def get_folder_candidates(
    session: DbSessionDep,
    folder_id: UUID,
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
) -> FolderCandidatesList:
    """Получает кандидатов в папке"""
    
    # Проверяем, что папка существует
    folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    candidates, total = await folders_repo.get_folder_candidates(
        session=session,
        folder_id=folder_id,
        page=page,
        per_page=per_page,
    )
    
    return FolderCandidatesList(
        candidates=[_folder_candidate_to_schema(candidate) for candidate in candidates],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.put(
    "/{folder_id}/candidates/{candidate_id}",
    response_model=FolderCandidateOut,
    summary="Обновить информацию о кандидате в папке",
    description="Обновляет заметки о кандидате в папке"
)
async def update_folder_candidate(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_id: UUID,
    candidate_id: UUID,
    candidate_data: CandidateUpdateInFolder,
) -> FolderCandidateOut:
    """Обновляет информацию о кандидате в папке"""
    
    # Проверяем, что папка существует
    folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    # Проверяем права доступа
    if folder.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для редактирования кандидатов в папке"
        )
    
    folder_candidate = await folders_repo.update_folder_candidate(
        session=session,
        candidate_id=candidate_id,
        notes=candidate_data.notes,
    )
    
    if not folder_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кандидат не найден в папке"
        )
    
    return _folder_candidate_to_schema(folder_candidate)


@router.delete(
    "/{folder_id}/candidates/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить кандидата из папки",
    description="Удаляет кандидата из папки"
)
async def remove_candidate_from_folder(
    session: DbSessionDep,
    current_user: CurrentUserDep,
    folder_id: UUID,
    candidate_id: UUID,
):
    """Удаляет кандидата из папки"""
    
    # Проверяем, что папка существует
    folder = await folders_repo.get_folder_by_id(session, folder_id)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
    
    # Проверяем права доступа
    if folder.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления кандидатов из папки"
        )
    
    success = await folders_repo.remove_candidate_from_folder(session, candidate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кандидат не найден в папке"
        )
