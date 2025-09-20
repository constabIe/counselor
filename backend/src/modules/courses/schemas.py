from __future__ import annotations

from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from src.storages.sql.models import CourseLevel


class CourseOut(BaseModel):
    id: UUID = Field(..., description="ID курса")
    title: str = Field(..., description="Название курса")
    direction: str = Field(..., description="Направление")
    level: CourseLevel = Field(..., description="Уровень сложности")
    duration_hours: int = Field(..., description="Длительность в часах")
    description: Optional[str] = Field(None, description="Описание курса")
    created_at: datetime = Field(..., description="Дата создания")


class CourseCreate(BaseModel):
    title: str = Field(..., description="Название курса", max_length=255)
    direction: str = Field(..., description="Направление", max_length=255)
    level: CourseLevel = Field(..., description="Уровень сложности")
    duration_hours: int = Field(..., description="Длительность в часах", gt=0)
    description: Optional[str] = Field(None, description="Описание курса")


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Название курса", max_length=255)
    direction: Optional[str] = Field(None, description="Направление", max_length=255)
    level: Optional[CourseLevel] = Field(None, description="Уровень сложности")
    duration_hours: Optional[int] = Field(None, description="Длительность в часах", gt=0)
    description: Optional[str] = Field(None, description="Описание курса")
