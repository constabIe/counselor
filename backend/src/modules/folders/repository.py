from __future__ import annotations

import logging
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlmodel import select, func, and_, col
from sqlalchemy.ext.asyncio import AsyncSession

from src.storages.sql.models import Folder, FolderCandidate, User

logger = logging.getLogger(__name__)


async def create_folder(
    session: AsyncSession,
    name: str,
    job_id: UUID,
    created_by: UUID,
    description: Optional[str] = None,
) -> Folder:
    """Создает новую папку"""
    folder = Folder(
        name=name,
        description=description,
        job_id=job_id,
        created_by=created_by,
    )
    
    session.add(folder)
    await session.commit()
    await session.refresh(folder)
    
    return folder


async def get_folder_by_id(
    session: AsyncSession,
    folder_id: UUID,
) -> Optional[Folder]:
    """Получает папку по ID"""
    stmt = select(Folder).where(
        and_(
            Folder.id == folder_id,
            Folder.is_active == True
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_folders_by_job(
    session: AsyncSession,
    job_id: UUID,
    page: int = 1,
    per_page: int = 10,
) -> Tuple[List[Folder], int]:
    """Получает папки для конкретной вакансии"""
    # Подсчет общего количества
    count_stmt = select(func.count()).select_from(Folder).where(
        and_(
            Folder.job_id == job_id,
            Folder.is_active == True
        )
    )
    total_result = await session.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Получение папок с пагинацией
    stmt = select(Folder).where(
        and_(
            Folder.job_id == job_id,
            Folder.is_active == True
        )
    ).order_by(col(Folder.created_at).desc()).offset((page - 1) * per_page).limit(per_page)
    
    result = await session.execute(stmt)
    folders = list(result.scalars().all())
    
    return folders, total


async def get_folders_by_creator(
    session: AsyncSession,
    creator_id: UUID,
    page: int = 1,
    per_page: int = 10,
) -> Tuple[List[Folder], int]:
    """Получает папки, созданные конкретным пользователем"""
    # Подсчет общего количества
    count_stmt = select(func.count()).select_from(Folder).where(
        and_(
            Folder.created_by == creator_id,
            Folder.is_active == True
        )
    )
    total_result = await session.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Получение папок с пагинацией
    stmt = select(Folder).where(
        and_(
            Folder.created_by == creator_id,
            Folder.is_active == True
        )
    ).order_by(col(Folder.created_at).desc()).offset((page - 1) * per_page).limit(per_page)
    
    result = await session.execute(stmt)
    folders = list(result.scalars().all())
    
    return folders, total


async def update_folder(
    session: AsyncSession,
    folder_id: UUID,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Folder]:
    """Обновляет папку"""
    folder = await get_folder_by_id(session, folder_id)
    if not folder:
        return None
    
    if name is not None:
        folder.name = name
    if description is not None:
        folder.description = description
    
    folder.updated_at = datetime.utcnow()
    
    await session.commit()
    await session.refresh(folder)
    
    return folder


async def delete_folder(
    session: AsyncSession,
    folder_id: UUID,
) -> bool:
    """Удаляет папку (мягкое удаление)"""
    folder = await get_folder_by_id(session, folder_id)
    if not folder:
        return False
    
    folder.is_active = False
    folder.updated_at = datetime.utcnow()
    
    # Также деактивируем всех кандидатов в папке
    candidates_stmt = select(FolderCandidate).where(
        and_(
            FolderCandidate.folder_id == folder_id,
            FolderCandidate.is_active == True
        )
    )
    candidates_result = await session.execute(candidates_stmt)
    candidates = list(candidates_result.scalars().all())
    
    for candidate in candidates:
        candidate.is_active = False
    
    await session.commit()
    return True


async def add_candidate_to_folder(
    session: AsyncSession,
    folder_id: UUID,
    user_id: UUID,
    added_by: UUID,
    notes: Optional[str] = None,
) -> Optional[FolderCandidate]:
    """Добавляет кандидата в папку"""
    # Проверяем, что папка существует
    folder = await get_folder_by_id(session, folder_id)
    if not folder:
        return None
    
    # Проверяем, что кандидат не уже в папке
    existing_stmt = select(FolderCandidate).where(
        and_(
            FolderCandidate.folder_id == folder_id,
            FolderCandidate.user_id == user_id,
            FolderCandidate.is_active == True
        )
    )
    existing_result = await session.execute(existing_stmt)
    if existing_result.scalar_one_or_none():
        return None  # Кандидат уже в папке
    
    folder_candidate = FolderCandidate(
        folder_id=folder_id,
        user_id=user_id,
        added_by=added_by,
        notes=notes,
    )
    
    session.add(folder_candidate)
    await session.commit()
    await session.refresh(folder_candidate)
    
    return folder_candidate


async def get_folder_candidates(
    session: AsyncSession,
    folder_id: UUID,
    page: int = 1,
    per_page: int = 10,
) -> Tuple[List[FolderCandidate], int]:
    """Получает кандидатов в папке"""
    # Подсчет общего количества
    count_stmt = select(func.count()).select_from(FolderCandidate).where(
        and_(
            FolderCandidate.folder_id == folder_id,
            FolderCandidate.is_active == True
        )
    )
    total_result = await session.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Получение кандидатов с информацией о пользователе
    stmt = select(FolderCandidate, User).join(
        User, FolderCandidate.user_id == User.id # type: ignore
    ).where(
        and_(
            FolderCandidate.folder_id == folder_id,
            FolderCandidate.is_active == True
        )
    ).order_by(col(FolderCandidate.added_at).desc()).offset((page - 1) * per_page).limit(per_page)
    
    result = await session.execute(stmt)
    candidates_with_users = list(result.all())
    
    # Создаем список кандидатов с данными пользователей
    candidates = []
    for folder_candidate, user in candidates_with_users:
        # Добавляем данные пользователя к объекту кандидата
        folder_candidate.user_full_name = user.full_name
        folder_candidate.user_email = user.email
        candidates.append(folder_candidate)
    
    return candidates, total


async def get_folder_candidate_by_id(
    session: AsyncSession,
    candidate_id: UUID,
) -> Optional[FolderCandidate]:
    """Получает кандидата в папке по ID"""
    stmt = select(FolderCandidate).where(
        and_(
            FolderCandidate.id == candidate_id,
            FolderCandidate.is_active == True
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_folder_candidate(
    session: AsyncSession,
    candidate_id: UUID,
    notes: Optional[str] = None,
) -> Optional[FolderCandidate]:
    """Обновляет информацию о кандидате в папке"""
    candidate = await get_folder_candidate_by_id(session, candidate_id)
    if not candidate:
        return None
    
    if notes is not None:
        candidate.notes = notes
    
    await session.commit()
    await session.refresh(candidate)
    
    return candidate


async def remove_candidate_from_folder(
    session: AsyncSession,
    candidate_id: UUID,
) -> bool:
    """Удаляет кандидата из папки (мягкое удаление)"""
    candidate = await get_folder_candidate_by_id(session, candidate_id)
    if not candidate:
        return False
    
    candidate.is_active = False
    
    await session.commit()
    return True


async def get_candidates_count_in_folder(
    session: AsyncSession,
    folder_id: UUID,
) -> int:
    """Получает количество кандидатов в папке"""
    stmt = select(func.count()).select_from(FolderCandidate).where(
        and_(
            FolderCandidate.folder_id == folder_id,
            FolderCandidate.is_active == True
        )
    )
    result = await session.execute(stmt)
    return result.scalar() or 0
