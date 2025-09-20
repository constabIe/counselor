from __future__ import annotations

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query

from src.modules.courses import repository as courses_repo
from src.modules.courses.schemas import CourseOut, CourseCreate, CourseUpdate
from src.storages.sql.dependencies import DbSessionDep
from src.modules.users.dependencies import CurrentUserDep
from src.storages.sql.models import CourseLevel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
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
