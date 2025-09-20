from __future__ import annotations

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import FileResponse

from src.modules.cv import repository as cv_repo
from src.modules.badges import service as badge_service
from src.modules.users import repository as user_repo
from src.modules.cv.schemas import CVUploadResponse, CVOut, CVUpdate, CVUpdateResponse
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep
from src.utils.file_storage import save_cv_file, delete_cv_file, get_file_size_mb

logger = logging.getLogger(__name__)

# XP значения для различных полей CV
CV_FIELD_XP_VALUES = {
    # Важные поля (больше XP)
    "skills": 3,
    "experience_years": 2,
    "education": 3,
    "jobs": 4,
    "current_role": 2,
    "responsibilities": 2,
    "competencies": 4,
    
    # Средние поля
    "additional_education": 2,
    "languages": 2,
    "department": 1,
    "specialization": 2,
    
    # Простые поля
    "age": 1,
    "grade": 1,
    "comments": 1,
    "tags": 1,
    "career_path": 2,
}

def calculate_cv_update_xp(update_fields: dict) -> int:
    """Рассчитывает XP за обновление полей CV"""
    total_xp = 0
    
    for field_name in update_fields.keys():
        # Получаем XP за поле, по умолчанию 1 XP
        field_xp = CV_FIELD_XP_VALUES.get(field_name, 1)
        total_xp += field_xp
    
    # Бонус за обновление множественных полей
    field_count = len(update_fields)
    if field_count >= 5:
        total_xp += 5  # Бонус за обновление 5+ полей
    elif field_count >= 3:
        total_xp += 2  # Бонус за обновление 3+ полей
    
    return total_xp

router = APIRouter(
    prefix="/cv",
    tags=["CV Management"],
)

@router.post(
    "/upload",
    response_model=CVUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить CV",
    description="Загружает PDF файл с резюме для анализа"
)
async def upload_cv(
    current_user: CurrentUserDep,
    session: DbSessionDep,
    file: UploadFile = File(..., description="PDF файл с резюме"),
) -> CVUploadResponse:
    """Загружает CV файл"""
    
    logger.info(f"Попытка загрузки файла: {file.filename}, content_type: {file.content_type}, size: {file.size}")
    
    # Валидация файла
    if not file.filename:
        logger.error("Имя файла не указано")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя файла не указано"
        )
    
    # Проверяем тип файла
    if not file.content_type or not file.content_type.startswith(('application/pdf', 'application/octet-stream')):
        # Также проверяем расширение файла
        if not file.filename.lower().endswith('.pdf'):
            logger.error(f"Неподдерживаемый тип файла: {file.content_type}, имя: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Поддерживаются только PDF файлы"
            )
    
    # Проверяем размер файла (максимум 10MB)
    if file.size and file.size > 10 * 1024 * 1024:
        logger.error(f"Файл слишком большой: {file.size} байт")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Размер файла не должен превышать 10MB"
        )
    
    try:
        # Сохраняем файл
        filename, file_path, file_size = await save_cv_file(file)
        
        # Создаем запись в БД
        cv = await cv_repo.create_cv(
            session,
            user_id=current_user.id,
            filename=filename,
            original_filename=file.filename or "cv.pdf",
            file_path=file_path,
            file_size=file_size,
            content_type=file.content_type or "application/pdf",
        )
        
        # Проверяем и выдаем бейджи за загрузку CV
        await badge_service.badge_service.check_and_award_badges(
            session, current_user.id, "cv_uploaded"
        )
        
        # Дополнительно начисляем XP за загрузку CV (независимо от бейджей)
        upload_xp = 5  # 5 XP за загрузку
        await user_repo.add_xp_to_user(session, current_user.id, upload_xp)
        
        await session.commit()
        
        return CVUploadResponse(
            id=cv.id,
            filename=cv.filename,
            original_filename=cv.original_filename,
            file_size=cv.file_size,
            uploaded_at=cv.uploaded_at,
            analysis_status=cv.analysis_status,
            xp_earned=upload_xp,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при загрузке файла: {str(e)}"
        )


@router.get(
    "/stats",
    summary="Статистика CV",
    description="Получает статистику CV текущего пользователя"
)
async def get_cv_stats(
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> dict:
    """Получает статистику CV пользователя"""
    
    active_count = await cv_repo.get_user_active_cv_count(session, current_user.id)
    all_cvs = await cv_repo.get_user_cvs(session, current_user.id, include_inactive=True)
    deleted_cvs = await cv_repo.get_user_deleted_cvs(session, current_user.id)
    
    return {
        "active_cv_count": active_count,
        "total_cv_count": len(all_cvs),
        "deleted_cv_count": len(deleted_cvs),
        "current_active_cv": all_cvs[0].id if all_cvs and active_count > 0 else None
    }


@router.get(
    "/my",
    response_model=List[CVOut],
    summary="Мои CV",
    description="Получает список всех загруженных CV текущего пользователя"
)
async def get_my_cvs(
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> List[CVOut]:
    """Получает все CV текущего пользователя"""
    
    cvs = await cv_repo.get_user_cvs(session, current_user.id)
    
    return [
        CVOut(
            id=cv.id,
            user_id=cv.user_id,
            filename=cv.filename,
            original_filename=cv.original_filename,
            file_size=cv.file_size,
            uploaded_at=cv.uploaded_at,
            analysis_status=cv.analysis_status,
            skills=cv.skills,
            experience_years=cv.experience_years,
            education=cv.education,
            additional_education=cv.additional_education,
            jobs=cv.jobs,
            current_role=cv.current_role,
            responsibilities=cv.responsibilities,
            languages=cv.languages,
            age=cv.age,
            department=cv.department,
            grade=cv.grade,
            specialization=cv.specialization,
            competencies=cv.competencies,
            comments=cv.comments,
            rating=cv.rating,
            tags=cv.tags,
            career_path=cv.career_path,
        )
        for cv in cvs
    ]


@router.get(
    "/deleted",
    response_model=List[CVOut],
    summary="Удаленные CV",
    description="Получает список всех удаленных (неактивных) CV текущего пользователя"
)
async def get_deleted_cvs(
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> List[CVOut]:
    """Получает все удаленные CV текущего пользователя"""
    
    cvs = await cv_repo.get_user_deleted_cvs(session, current_user.id)
    
    return [
        CVOut(
            id=cv.id,
            user_id=cv.user_id,
            filename=cv.filename,
            original_filename=cv.original_filename,
            file_size=cv.file_size,
            uploaded_at=cv.uploaded_at,
            analysis_status=cv.analysis_status,
            skills=cv.skills,
            experience_years=cv.experience_years,
            education=cv.education,
            additional_education=cv.additional_education,
            jobs=cv.jobs,
            current_role=cv.current_role,
            responsibilities=cv.responsibilities,
            languages=cv.languages,
            age=cv.age,
            department=cv.department,
            grade=cv.grade,
            specialization=cv.specialization,
            competencies=cv.competencies,
            comments=cv.comments,
            rating=cv.rating,
            tags=cv.tags,
            career_path=cv.career_path,
        )
        for cv in cvs
    ]


@router.get(
    "/{cv_id}",
    response_model=CVOut,
    summary="Получить CV",
    description="Получает информацию о конкретном CV"
)
async def get_cv(
    cv_id: UUID,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> CVOut:
    """Получает информацию о CV"""
    
    cv = await cv_repo.get_cv_by_id(session, cv_id)
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV не найдено"
        )
    
    # Проверяем права доступа
    if cv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа к этому CV"
        )
    
    return CVOut(
        id=cv.id,
        user_id=cv.user_id,
        filename=cv.filename,
        original_filename=cv.original_filename,
        file_size=cv.file_size,
        uploaded_at=cv.uploaded_at,
        analysis_status=cv.analysis_status,
        skills=cv.skills,
        experience_years=cv.experience_years,
        education=cv.education,
        additional_education=cv.additional_education,
        jobs=cv.jobs,
        current_role=cv.current_role,
        responsibilities=cv.responsibilities,
        languages=cv.languages,
        age=cv.age,
        department=cv.department,
        grade=cv.grade,
        specialization=cv.specialization,
        competencies=cv.competencies,
        comments=cv.comments,
        rating=cv.rating,
        tags=cv.tags,
        career_path=cv.career_path,
    )


@router.get(
    "/{cv_id}/download",
    response_class=FileResponse,
    summary="Скачать CV",
    description="Скачивает оригинальный PDF файл CV"
)
async def download_cv(
    cv_id: UUID,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> FileResponse:
    """Скачивает CV файл"""
    
    cv = await cv_repo.get_cv_by_id(session, cv_id)
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV не найдено"
        )
    
    # Проверяем права доступа
    if cv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для доступа к этому CV"
        )
    
    # Проверяем существование файла
    import os
    if not os.path.exists(cv.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден на сервере"
        )
    
    return FileResponse(
        path=cv.file_path,
        filename=cv.original_filename,
        media_type=cv.content_type,
    )


@router.delete(
    "/{cv_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить CV",
    description="Удаляет CV (мягкое удаление)",
    response_model=None
)
async def delete_cv(
    cv_id: UUID,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> None:
    """Удаляет CV"""
    
    success = await cv_repo.delete_cv(session, cv_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV не найдено или недостаточно прав"
        )


@router.patch(
    "/{cv_id}",
    response_model=CVUpdateResponse,
    summary="Обновить поля CV",
    description="Обновляет указанные поля CV и возвращает пересчитанный рейтинг"
)
async def update_cv(
    cv_id: UUID,
    cv_update: CVUpdate,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> CVUpdateResponse:
    """Обновляет поля CV"""
    
    # Получаем только заполненные поля для обновления
    update_fields = {
        field_name: field_value 
        for field_name, field_value in cv_update.model_dump(exclude_unset=True).items()
        if field_value is not None
    }
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать хотя бы одно поле для обновления"
        )
    
    # Обновляем CV
    updated_cv = await cv_repo.update_cv_fields(
        session, 
        cv_id, 
        current_user.id, 
        **update_fields
    )
    
    if not updated_cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV не найдено или недостаточно прав"
        )
    
    # Начисляем XP за обновление CV
    xp_for_update = calculate_cv_update_xp(update_fields)
    await user_repo.add_xp_to_user(session, current_user.id, xp_for_update)
    
    # Получаем примерное количество обновлений для проверки бейджей
    update_count = await user_repo.increment_user_cv_updates(session, current_user.id)
    
    # Проверяем и выдаем бейджи за обновление профиля
    await badge_service.badge_service.check_and_award_badges(
        session, current_user.id, "profile_updated", cv_update_count=update_count
    )
    
    await session.commit()
    
    return CVUpdateResponse(
        id=updated_cv.id,
        rating=updated_cv.rating,
        updated_fields=list(update_fields.keys()),
        xp_earned=xp_for_update  # Добавим информацию о заработанном XP
    )


@router.patch(
    "/{cv_id}/restore",
    response_model=CVOut,
    summary="Восстановить CV",
    description="Восстанавливает удаленное CV (делает его снова активным)"
)
async def restore_cv(
    cv_id: UUID,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> CVOut:
    """Восстанавливает удаленное CV"""
    
    # Получаем CV (включая неактивные)
    cv = await cv_repo.get_cv_by_id(session, cv_id, include_inactive=True)
    
    if not cv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CV не найдено"
        )
    
    # Проверяем права доступа
    if cv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для восстановления этого CV"
        )
    
    # Проверяем, что CV действительно удалено
    if cv.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CV уже активно"
        )
    
    # Восстанавливаем CV
    restored_cv = await cv_repo.restore_cv(session, cv_id)
    
    if not restored_cv:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при восстановлении CV"
        )
    
    return CVOut(
        id=restored_cv.id,
        user_id=restored_cv.user_id,
        filename=restored_cv.filename,
        original_filename=restored_cv.original_filename,
        file_size=restored_cv.file_size,
        uploaded_at=restored_cv.uploaded_at,
        analysis_status=restored_cv.analysis_status,
        skills=restored_cv.skills,
        experience_years=restored_cv.experience_years,
        education=restored_cv.education,
        additional_education=restored_cv.additional_education,
        jobs=restored_cv.jobs,
        current_role=restored_cv.current_role,
        responsibilities=restored_cv.responsibilities,
        languages=restored_cv.languages,
        age=restored_cv.age,
        department=restored_cv.department,
        grade=restored_cv.grade,
        specialization=restored_cv.specialization,
        competencies=restored_cv.competencies,
        comments=restored_cv.comments,
        rating=restored_cv.rating,
        tags=restored_cv.tags,
        career_path=restored_cv.career_path,
    )
