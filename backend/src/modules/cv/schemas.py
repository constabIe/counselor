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


class CVAnalysisResult(BaseModel):
    id: UUID = Field(..., description="ID CV")
    parsed_text: str = Field(..., description="Извлеченный текст")
    skills: list[str] = Field(..., description="Список навыков")
    experience_years: int = Field(..., description="Количество лет опыта")
    education: dict = Field(..., description="Информация об образовании")
    summary: str = Field(..., description="Краткое резюме кандидата")
