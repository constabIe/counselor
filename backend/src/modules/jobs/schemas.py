from __future__ import annotations

from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from src.storages.sql.models import JobLevel, JobStatus, EmploymentType


class JobCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Название вакансии")
    department: str = Field(..., max_length=255, description="Отдел/направление")
    level: JobLevel = Field(..., description="Уровень позиции")
    employment_type: EmploymentType = Field(default=EmploymentType.FULL_TIME, description="Тип занятости")
    location: Optional[str] = Field(None, max_length=255, description="Местоположение")
    remote_available: bool = Field(default=False, description="Доступна ли удаленная работа")
    description: str = Field(..., description="Подробное описание вакансии")
    requirements: str = Field(..., description="Требования к кандидату")
    responsibilities: str = Field(..., description="Обязанности")
    required_skills: Optional[list[str]] = Field(None, description="Требуемые навыки")
    min_experience_years: Optional[int] = Field(None, ge=0, description="Минимальный опыт работы в годах")
    max_experience_years: Optional[int] = Field(None, ge=0, description="Максимальный опыт работы в годах")
    average_salary: Optional[int] = Field(None, ge=0, description="Средняя предлагаемая зарплата")
    salary_currency: str = Field(default="RUB", max_length=10, description="Валюта зарплаты")


class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255, description="Название вакансии")
    department: Optional[str] = Field(None, max_length=255, description="Отдел/направление")
    level: Optional[JobLevel] = Field(None, description="Уровень позиции")
    employment_type: Optional[EmploymentType] = Field(None, description="Тип занятости")
    location: Optional[str] = Field(None, max_length=255, description="Местоположение")
    remote_available: Optional[bool] = Field(None, description="Доступна ли удаленная работа")
    description: Optional[str] = Field(None, description="Подробное описание вакансии")
    requirements: Optional[str] = Field(None, description="Требования к кандидату")
    responsibilities: Optional[str] = Field(None, description="Обязанности")
    required_skills: Optional[list[str]] = Field(None, description="Требуемые навыки")
    min_experience_years: Optional[int] = Field(None, ge=0, description="Минимальный опыт работы в годах")
    max_experience_years: Optional[int] = Field(None, ge=0, description="Максимальный опыт работы в годах")
    average_salary: Optional[int] = Field(None, ge=0, description="Средняя предлагаемая зарплата")
    salary_currency: Optional[str] = Field(None, max_length=10, description="Валюта зарплаты")
    status: Optional[JobStatus] = Field(None, description="Статус вакансии")


class JobOut(BaseModel):
    id: UUID = Field(..., description="ID вакансии")
    title: str = Field(..., description="Название вакансии")
    department: str = Field(..., description="Отдел/направление")
    level: JobLevel = Field(..., description="Уровень позиции")
    employment_type: EmploymentType = Field(..., description="Тип занятости")
    location: Optional[str] = Field(..., description="Местоположение")
    remote_available: bool = Field(..., description="Доступна ли удаленная работа")
    description: str = Field(..., description="Подробное описание вакансии")
    requirements: str = Field(..., description="Требования к кандидату")
    responsibilities: str = Field(..., description="Обязанности")
    required_skills: Optional[list[str]] = Field(..., description="Требуемые навыки")
    min_experience_years: Optional[int] = Field(..., description="Минимальный опыт работы в годах")
    max_experience_years: Optional[int] = Field(..., description="Максимальный опыт работы в годах")
    average_salary: Optional[int] = Field(..., description="Средняя предлагаемая зарплата")
    salary_currency: str = Field(..., description="Валюта зарплаты")
    status: JobStatus = Field(..., description="Статус вакансии")
    created_by: UUID = Field(..., description="Кто создал вакансию")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    published_at: Optional[datetime] = Field(..., description="Дата публикации")


class JobList(BaseModel):
    jobs: list[JobOut] = Field(..., description="Список вакансий")
    total: int = Field(..., description="Общее количество вакансий")
    page: int = Field(..., description="Текущая страница")
    per_page: int = Field(..., description="Количество элементов на странице")
