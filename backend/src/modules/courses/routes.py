from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query

from src.modules.courses import repository as courses_repo
from src.modules.courses import enrollment_repository as enrollment_repo
from src.modules.courses.schemas import CourseOut, CourseCreate, CourseUpdate
from src.modules.courses.enrollment_schemas import (
    EnrollmentCreate, EnrollmentOut, EnrollmentUpdate, 
    EnrollmentResponse, UserEnrollmentsSummary
)
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep
from src.storages.sql.models import CourseLevel, EnrollmentStatus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.get(
    "/my-enrollments",
    response_model=UserEnrollmentsSummary,
    summary="Мои записи на курсы",
    description="Получает все записи текущего пользователя на курсы"
)
async def get_my_enrollments(
    current_user: CurrentUserDep,
    session: DbSessionDep,
    status: Optional[EnrollmentStatus] = Query(None, description="Фильтр по статусу"),
) -> UserEnrollmentsSummary:
    """Получает записи пользователя на курсы"""
    
    # Получаем записи с информацией о курсах
    enrollments_with_courses = await enrollment_repo.get_user_enrollments(
        session, current_user.id, status
    )
    
    # Получаем статистику по статусам
    status_counts = await enrollment_repo.get_enrollment_counts_by_status(
        session, current_user.id
    )
    
    # Формируем список записей
    enrollments = [
        EnrollmentOut(
            id=enrollment.id,
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            course_title=course.title,
            course_direction=course.direction,
            course_level=course.level,
            course_duration_hours=course.duration_hours,
            status=enrollment.status,
            enrolled_at=enrollment.enrolled_at,
            started_at=enrollment.started_at,
        )
        for enrollment, course in enrollments_with_courses
    ]
    
    return UserEnrollmentsSummary(
        enrollments=enrollments,
        total_count=len(enrollments),
        enrolled_count=status_counts["enrolled"],
        started_count=status_counts["started"],
        completed_count=status_counts["completed"],
    )


@router.get(
    "/",
    response_model=List[CourseOut],
    summary="Получить все курсы",
    description="Получает список всех доступных курсов с возможностью фильтрации"
)
async def get_courses(
    session: DbSessionDep,
    direction: Optional[str] = Query(None, description="Фильтр по направлению"),
    level: Optional[CourseLevel] = Query(None, description="Фильтр по уровню"),
) -> List[CourseOut]:
    """Получает все курсы"""
    
    courses = await courses_repo.get_all_courses(
        session, 
        direction=direction, 
        level=level
    )
    
    return [
        CourseOut(
            id=course.id,
            title=course.title,
            direction=course.direction,
            level=course.level,
            duration_hours=course.duration_hours,
            description=course.description,
            created_at=course.created_at,
        )
        for course in courses
    ]


@router.get(
    "/{course_id}",
    response_model=CourseOut,
    summary="Получить курс",
    description="Получает информацию о конкретном курсе"
)
async def get_course(
    course_id: UUID,
    session: DbSessionDep,
) -> CourseOut:
    """Получает информацию о курсе"""
    
    course = await courses_repo.get_course_by_id(session, course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Курс не найден"
        )
    
    return CourseOut(
        id=course.id,
        title=course.title,
        direction=course.direction,
        level=course.level,
        duration_hours=course.duration_hours,
        description=course.description,
        created_at=course.created_at,
    )


@router.get(
    "/direction/{direction}",
    response_model=List[CourseOut],
    summary="Получить курсы по направлению",
    description="Получает все курсы определенного направления"
)
async def get_courses_by_direction(
    direction: str,
    session: DbSessionDep,
) -> List[CourseOut]:
    """Получает курсы по направлению"""
    
    courses = await courses_repo.get_courses_by_direction(session, direction)
    
    return [
        CourseOut(
            id=course.id,
            title=course.title,
            direction=course.direction,
            level=course.level,
            duration_hours=course.duration_hours,
            description=course.description,
            created_at=course.created_at,
        )
        for course in courses
    ]


# @router.post(
#     "/",
#     response_model=CourseOut,
#     status_code=status.HTTP_201_CREATED,
#     summary="Создать курс",
#     description="Создает новый курс (только для администраторов)"
# )
# async def create_course(
#     course_data: CourseCreate,
#     current_user: CurrentUserDep,
#     session: DbSessionDep,
# ) -> CourseOut:
#     """Создает новый курс"""
    
#     # Проверяем права доступа (только админы могут создавать курсы)
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав для создания курса"
#         )
    
#     course = await courses_repo.create_course(
#         session,
#         title=course_data.title,
#         direction=course_data.direction,
#         level=course_data.level,
#         duration_hours=course_data.duration_hours,
#         description=course_data.description,
#     )
    
#     return CourseOut(
#         id=course.id,
#         title=course.title,
#         direction=course.direction,
#         level=course.level,
#         duration_hours=course.duration_hours,
#         description=course.description,
#         created_at=course.created_at,
#     )


# @router.patch(
#     "/{course_id}",
#     response_model=CourseOut,
#     summary="Обновить курс",
#     description="Обновляет информацию о курсе (только для администраторов)"
# )
# async def update_course(
#     course_id: UUID,
#     course_update: CourseUpdate,
#     current_user: CurrentUserDep,
#     session: DbSessionDep,
# ) -> CourseOut:
#     """Обновляет курс"""
    
#     # Проверяем права доступа
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав для обновления курса"
#         )
    
#     # Получаем только заполненные поля для обновления
#     update_fields = {
#         field_name: field_value 
#         for field_name, field_value in course_update.model_dump(exclude_unset=True).items()
#         if field_value is not None
#     }
    
#     if not update_fields:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Необходимо указать хотя бы одно поле для обновления"
#         )
    
#     # Обновляем курс
#     updated_course = await courses_repo.update_course(
#         session, 
#         course_id, 
#         **update_fields
#     )
    
#     if not updated_course:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Курс не найден"
#         )
    
#     return CourseOut(
#         id=updated_course.id,
#         title=updated_course.title,
#         direction=updated_course.direction,
#         level=updated_course.level,
#         duration_hours=updated_course.duration_hours,
#         description=updated_course.description,
#         created_at=updated_course.created_at,
#     )


# @router.delete(
#     "/{course_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Удалить курс",
#     description="Удаляет курс (только для администраторов)"
# )
# async def delete_course(
#     course_id: UUID,
#     current_user: CurrentUserDep,
#     session: DbSessionDep,
# ) -> None:
#     """Удаляет курс"""
    
#     # Проверяем права доступа
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Недостаточно прав для удаления курса"
#         )
    
#     success = await courses_repo.delete_course(session, course_id)
    
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Курс не найден"
#         )


# ========================= ENROLLMENT ROUTES =========================

@router.post(
    "/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Записаться на курс",
    description="Записывает текущего пользователя на курс"
)
async def enroll_to_course(
    enrollment_data: EnrollmentCreate,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> EnrollmentResponse:
    """Записывает пользователя на курс"""
    
    try:
        # Записываем на курс
        enrollment = await enrollment_repo.enroll_user_to_course(
            session, current_user.id, enrollment_data.course_id
        )
        
        # Получаем полную информацию о записи
        enrollment_with_course = await enrollment_repo.get_enrollment_by_id(
            session, enrollment.id
        )
        
        if not enrollment_with_course:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получении информации о записи"
            )
        
        enrollment_obj, course_obj = enrollment_with_course
        
        # Подсчитываем общее количество записей пользователя
        total_enrollments = await enrollment_repo.count_user_enrollments(
            session, current_user.id
        )
        
        return EnrollmentResponse(
            enrollment=EnrollmentOut(
                id=enrollment_obj.id,
                user_id=enrollment_obj.user_id,
                course_id=enrollment_obj.course_id,
                course_title=course_obj.title,
                course_direction=course_obj.direction,
                course_level=course_obj.level,
                course_duration_hours=course_obj.duration_hours,
                status=enrollment_obj.status,
                enrolled_at=enrollment_obj.enrolled_at,
                started_at=enrollment_obj.started_at,
            ),
            total_user_enrollments=total_enrollments
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch(
    "/enrollments/{enrollment_id}/status",
    response_model=EnrollmentOut,
    summary="Обновить статус записи",
    description="Обновляет статус записи на курс (например, начать изучение или завершить)"
)
async def update_enrollment_status(
    enrollment_id: UUID,
    enrollment_update: EnrollmentUpdate,
    current_user: CurrentUserDep,
    session: DbSessionDep,
) -> EnrollmentOut:
    """Обновляет статус записи на курс"""
    
    if not enrollment_update.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать новый статус"
        )
    
    # Обновляем статус
    updated_enrollment = await enrollment_repo.update_enrollment_status(
        session, enrollment_id, enrollment_update.status, current_user.id
    )
    
    if not updated_enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись на курс не найдена"
        )
    
    # Получаем полную информацию
    enrollment_with_course = await enrollment_repo.get_enrollment_by_id(
        session, enrollment_id, current_user.id
    )
    
    if not enrollment_with_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись на курс не найдена"
        )
    
    enrollment_obj, course_obj = enrollment_with_course
    
    return EnrollmentOut(
        id=enrollment_obj.id,
        user_id=enrollment_obj.user_id,
        course_id=enrollment_obj.course_id,
        course_title=course_obj.title,
        course_direction=course_obj.direction,
        course_level=course_obj.level,
        course_duration_hours=course_obj.duration_hours,
        status=enrollment_obj.status,
        enrolled_at=enrollment_obj.enrolled_at,
        started_at=enrollment_obj.started_at,
    )
