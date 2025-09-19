from __future__ import annotations

from uuid import UUID
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class GenerationFilters(BaseModel):
    """Фильтры для поиска сотрудников"""
    department: Optional[str] = Field(None, description="Департамент/отдел")
    experience_years_min: Optional[int] = Field(None, description="Минимальный опыт работы")
    experience_years_max: Optional[int] = Field(None, description="Максимальный опыт работы")
    skills: Optional[List[str]] = Field(None, description="Требуемые навыки")
    level: Optional[str] = Field(None, description="Уровень специалиста")
    languages: Optional[List[str]] = Field(None, description="Знание языков")
    education_level: Optional[str] = Field(None, description="Уровень образования")
    age_min: Optional[int] = Field(None, description="Минимальный возраст")
    age_max: Optional[int] = Field(None, description="Максимальный возраст")


class GenerationRequest(BaseModel):
    """Запрос на генерацию сотрудников"""
    query: str = Field(..., description="Текстовый запрос HR", min_length=1)
    filters: Optional[GenerationFilters] = Field(None, description="Фильтры поиска")


class EmployeeBasic(BaseModel):
    """Базовая информация о сотруднике"""
    id: UUID = Field(..., description="ID сотрудника (CV)")
    name: Optional[str] = Field(None, description="Имя сотрудника")
    department: Optional[str] = Field(None, description="Отдел/департамент")
    experience_years: Optional[int] = Field(None, description="Опыт работы в годах")
    rating: Optional[float] = Field(None, description="Рейтинг сотрудника")
    skills: Optional[List[str]] = Field(None, description="Основные навыки")
    match_score: Optional[float] = Field(None, description="Степень соответствия запросу (0-1)")


class GenerationResponse(BaseModel):
    """Ответ на запрос генерации"""
    query: str = Field(..., description="Исходный запрос")
    generated_tags: List[str] = Field(..., description="Сгенерированные теги от ИИ")
    employees: List[EmployeeBasic] = Field(..., description="Найденные сотрудники")
    total_found: int = Field(..., description="Общее количество найденных сотрудников")


class AIGenerationRequest(BaseModel):
    """Запрос к AI модулю для генерации тегов"""
    combined_query: str = Field(..., description="Объединенный запрос с фильтрами")


class AIGenerationResponse(BaseModel):
    """Ответ от AI модуля"""
    tags: List[str] = Field(..., description="Сгенерированные теги")
    confidence: float = Field(default=1.0, description="Уверенность модели (0-1)")
