from __future__ import annotations

import logging
from typing import List
import json

from src.modules.generation.schemas import AIGenerationRequest, AIGenerationResponse

logger = logging.getLogger(__name__)


class AIService:
    """Сервис для взаимодействия с AI API (заглушка)"""
    
    @staticmethod
    async def generate_tags(request: AIGenerationRequest) -> AIGenerationResponse:
        """
        Генерирует теги на основе запроса
        ВНИМАНИЕ: Это заглушка! В будущем здесь будет реальный вызов AI API
        """
        
        logger.info(f"AI запрос: {request.combined_query}")
        
        # Простейшая заглушка - извлекаем ключевые слова из запроса
        query_lower = request.combined_query.lower()
        
        # Предопределенные теги для демонстрации
        mock_tags = []
        
        # IT навыки
        if any(word in query_lower for word in ['python', 'разработчик', 'программист', 'developer']):
            mock_tags.extend(['python', 'programming', 'backend', 'web-development'])
        
        if any(word in query_lower for word in ['frontend', 'react', 'javascript', 'vue']):
            mock_tags.extend(['frontend', 'javascript', 'react', 'html', 'css'])
        
        if any(word in query_lower for word in ['devops', 'docker', 'kubernetes', 'ci/cd']):
            mock_tags.extend(['devops', 'docker', 'kubernetes', 'ci-cd', 'automation'])
        
        # HR навыки
        if any(word in query_lower for word in ['hr', 'рекрутер', 'кадры', 'персонал']):
            mock_tags.extend(['hr', 'recruitment', 'personnel-management', 'talent-acquisition'])
        
        # Менеджмент
        if any(word in query_lower for word in ['менеджер', 'управление', 'проект', 'team lead']):
            mock_tags.extend(['management', 'project-management', 'team-leadership', 'planning'])
        
        # Маркетинг
        if any(word in query_lower for word in ['маркетинг', 'seo', 'smm', 'реклама']):
            mock_tags.extend(['marketing', 'digital-marketing', 'seo', 'social-media'])
        
        # Уровни опыта
        if any(word in query_lower for word in ['junior', 'начинающий', 'стажер']):
            mock_tags.extend(['junior', 'entry-level'])
        elif any(word in query_lower for word in ['senior', 'старший', 'ведущий']):
            mock_tags.extend(['senior', 'expert-level'])
        elif any(word in query_lower for word in ['middle', 'средний']):
            mock_tags.extend(['middle', 'intermediate'])
        
        # Языки
        if any(word in query_lower for word in ['английский', 'english']):
            mock_tags.append('english')
        if any(word in query_lower for word in ['немецкий', 'german']):
            mock_tags.append('german')
        
        # Если ничего не найдено, добавляем общие теги
        if not mock_tags:
            mock_tags = ['general', 'professional', 'experienced']
        
        # Убираем дубликаты
        unique_tags = list(set(mock_tags))
        
        logger.info(f"Сгенерированные теги: {unique_tags}")
        
        return AIGenerationResponse(
            tags=unique_tags,
            confidence=0.85  # Мок-значение уверенности
        )
