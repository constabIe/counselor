from __future__ import annotations

import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.generation.schemas import (
    GenerationRequest, 
    GenerationResponse, 
    EmployeeBasic,
    AIGenerationRequest,
    GenerationFilters
)
from src.modules.generation.ai_service import AIService
from src.modules.generation import repository as gen_repo

logger = logging.getLogger(__name__)


class GenerationService:
    """Сервис для генерации сотрудников"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_employees(
        self, 
        session: AsyncSession, 
        request: GenerationRequest
    ) -> GenerationResponse:
        """Основной метод генерации сотрудников"""
        
        logger.info(f"Запрос генерации: '{request.query}' с фильтрами: {request.filters}")
        
        # 1. Формируем объединенный запрос для AI
        combined_query = self._build_combined_query(request)
        
        # 2. Отправляем запрос в AI сервис для получения тегов
        ai_request = AIGenerationRequest(combined_query=combined_query)
        ai_response = await self.ai_service.generate_tags(ai_request)
        
        # 3. Ищем сотрудников по полученным тегам
        filters = request.filters or GenerationFilters(
            department=None,
            experience_years_min=None,
            experience_years_max=None,
            skills=None,
            level=None,
            languages=None,
            education_level=None,
            age_min=None,
            age_max=None
        )
        
        employees = await gen_repo.search_employees_by_tags(
            session=session,
            tags=ai_response.tags,
            filters=filters,
            limit=50
        )
        
        # 4. Сортируем по match_score
        employees.sort(key=lambda x: (x.match_score or 0, x.rating or 0), reverse=True)
        
        logger.info(f"Найдено {len(employees)} сотрудников")
        
        return GenerationResponse(
            query=request.query,
            generated_tags=ai_response.tags,
            employees=employees,
            total_found=len(employees)
        )
    
    def _build_combined_query(self, request: GenerationRequest) -> str:
        """Формирует объединенный запрос из текста и фильтров"""
        
        parts = [request.query]
        
        # Проверяем, что фильтры существуют
        if not request.filters:
            return request.query
        
        filters = request.filters
        
        # Добавляем фильтры в текстовом виде
        if filters.department:
            parts.append(f"департамент: {filters.department}")
        
        if filters.experience_years_min is not None:
            parts.append(f"опыт от {filters.experience_years_min} лет")
        
        if filters.experience_years_max is not None:
            parts.append(f"опыт до {filters.experience_years_max} лет")
        
        if filters.skills:
            parts.append(f"навыки: {', '.join(filters.skills)}")
        
        if filters.level:
            parts.append(f"уровень: {filters.level}")
        
        if filters.languages:
            parts.append(f"языки: {', '.join(filters.languages)}")
        
        if filters.education_level:
            parts.append(f"образование: {filters.education_level}")
        
        if filters.age_min is not None:
            parts.append(f"возраст от {filters.age_min}")
        
        if filters.age_max is not None:
            parts.append(f"возраст до {filters.age_max}")
        
        combined = ". ".join(parts)
        logger.debug(f"Объединенный запрос: {combined}")
        
        return combined
