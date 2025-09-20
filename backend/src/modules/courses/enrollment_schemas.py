from __future__ import annotations

from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from src.storages.sql.models import EnrollmentStatus, CourseLevel


class EnrollmentCreate(BaseModel):
    course_id: UUID = Field(..., description="ID курса для записи")


class EnrollmentOut(BaseModel):
    id: UUID = Field(..., description="ID записи")
    user_id: UUID = Field(..., description="ID пользователя")
    course_id: UUID = Field(..., description="ID курса")
    course_title: str = Field(..., description="Название курса")
    course_direction: str = Field(..., description="Направление курса")
    course_level: CourseLevel = Field(..., description="Уровень курса")
    course_duration_hours: int = Field(..., description="Длительность курса в часах")
    status: EnrollmentStatus = Field(..., description="Статус")
    enrolled_at: datetime = Field(..., description="Дата записи")
    started_at: Optional[datetime] = Field(None, description="Дата начала изучения")


class EnrollmentUpdate(BaseModel):
    status: Optional[EnrollmentStatus] = Field(None, description="Новый статус")


class EnrollmentResponse(BaseModel):
    enrollment: EnrollmentOut = Field(..., description="Информация о записи")
    total_user_enrollments: int = Field(..., description="Общее количество записей пользователя на курсы")


class UserEnrollmentsSummary(BaseModel):
    enrollments: list[EnrollmentOut] = Field(..., description="Список записей на курсы")
    total_count: int = Field(..., description="Общее количество записей")
    enrolled_count: int = Field(..., description="Количество записанных курсов")
    started_count: int = Field(..., description="Количество начатых курсов")
    completed_count: int = Field(..., description="Количество завершенных курсов")
