from __future__ import annotations

from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CVUploadResponse(BaseModel):
    id: UUID = Field(..., description="ID загруженного CV")
    filename: str = Field(..., description="Имя файла")
    original_filename: str = Field(..., description="Оригинальное имя файла")
    file_size: int = Field(..., description="Размер файла в байтах")
    uploaded_at: datetime = Field(..., description="Время загрузки")
    analysis_status: str = Field(..., description="Статус анализа")


class CVOut(BaseModel):
    id: UUID = Field(..., description="ID CV")
    user_id: UUID = Field(..., description="ID пользователя")
    filename: str = Field(..., description="Имя файла")
    original_filename: str = Field(..., description="Оригинальное имя файла")
    file_size: int = Field(..., description="Размер файла в байтах")
    uploaded_at: datetime = Field(..., description="Время загрузки")
    analysis_status: str = Field(..., description="Статус анализа")
    
    # Результаты анализа
    skills: Optional[str] = Field(None, description="Навыки (JSON)")  
    experience_years: Optional[int] = Field(None, description="Лет опыта")  
    education: Optional[str] = Field(None, description="Образование (JSON)")  
    additional_education: Optional[str] = Field(None, description="Курсы и сертификаты (JSON)")  
    jobs: Optional[str] = Field(None, description="Предыдущие работы (JSON)")  
    current_role: Optional[str] = Field(None, description="Текущая роль/должность (JSON)")  
    responsibilities: Optional[str] = Field(None, description="Обязанности в текущей роли (JSON)")  
    languages: Optional[str] = Field(None, description="Языки (JSON)")  
    age: Optional[int] = Field(None, description="Возраст кандидата")  
    department: Optional[str] = Field(None, description="Подразделение/направление")  
    grade: Optional[str] = Field(None, description="Грейд (если есть)")  
    specialization: Optional[str] = Field(None, description="Специализация (например, L1 Support)")  
    competencies: Optional[str] = Field(None, description="Компетенции с уровнями (JSON)")  
    comments: Optional[str] = Field(None, description="Дополнительное описание (свободный текст)")  
    
    # Метаданные от ИИ
    rating: Optional[float] = Field(None, description="Рейтинг от ИИ (0-10)")  
    tags: Optional[str] = Field(None, description="Специальные теги от ИИ (JSON)")  
    career_path: Optional[str] = Field(None, description="Предлагаемая карьерная траектория (JSON)")


class CVUpdate(BaseModel):
    skills: Optional[str] = Field(None, description="Навыки (JSON)")
    experience_years: Optional[int] = Field(None, description="Лет опыта")
    education: Optional[str] = Field(None, description="Образование (JSON)")
    additional_education: Optional[str] = Field(None, description="Курсы и сертификаты (JSON)")
    jobs: Optional[str] = Field(None, description="Предыдущие работы (JSON)")
    current_role: Optional[str] = Field(None, description="Текущая роль/должность (JSON)")
    responsibilities: Optional[str] = Field(None, description="Обязанности в текущей роли (JSON)")
    languages: Optional[str] = Field(None, description="Языки (JSON)")
    age: Optional[int] = Field(None, description="Возраст кандидата")
    department: Optional[str] = Field(None, description="Подразделение/направление")
    grade: Optional[str] = Field(None, description="Грейд (если есть)")
    specialization: Optional[str] = Field(None, description="Специализация (например, L1 Support)")
    competencies: Optional[str] = Field(None, description="Компетенции с уровнями (JSON)")
    comments: Optional[str] = Field(None, description="Дополнительное описание (свободный текст)")
    tags: Optional[str] = Field(None, description="Специальные теги (JSON)")
    career_path: Optional[str] = Field(None, description="Предлагаемая карьерная траектория (JSON)")


class CVUpdateResponse(BaseModel):
    id: UUID = Field(..., description="ID CV")
    rating: Optional[float] = Field(None, description="Обновленный рейтинг от ИИ (0-10)")
    updated_fields: list[str] = Field(..., description="Список обновленных полей")


class CVAnalysisResult(BaseModel):
    id: UUID = Field(..., description="ID CV")
    parsed_text: str = Field(..., description="Извлеченный текст")
    skills: list[str] = Field(..., description="Список навыков")
    experience_years: int = Field(..., description="Количество лет опыта")
    education: dict = Field(..., description="Информация об образовании")
    age: Optional[int] = Field(None, description="Возраст кандидата")
    jobs: list[dict] = Field(default_factory=list, description="Предыдущие работы")
    languages: list[dict] = Field(default_factory=list, description="Знание языков")
    rating: float = Field(..., description="Рейтинг кандидата от ИИ (0-10)")
    tags: list[str] = Field(default_factory=list, description="Специальные теги от ИИ")
    summary: str = Field(..., description="Краткое резюме кандидата")
