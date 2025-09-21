import os
import aiohttp
import asyncio
import json
import logging
from typing import AsyncGenerator

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        # Читаем конфигурацию из переменных окружения
        self.api_url = os.getenv("LLM_API_URL", "https://llm.t1v.scibox.tech/completions")
        self.api_token = os.getenv("LLM_API_TOKEN", "sk-oWtKHDq9UET7fCG0JaJDWQ")
        self.model = os.getenv("LLM_MODEL", "Qwen2.5-72B-Instruct-AWQ")
        
        logger.info(f"LLM Service initialized with URL: {self.api_url}")
    
    async def generate_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Генерирует ответ от LLM модели потоково"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": True
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"LLM API error: {response.status} - {error_text}")
                        yield f"Ошибка LLM API: {response.status} - {error_text}"
                        return
                    
                    async for line in response.content:
                        if line:
                            try:
                                line_str = line.decode('utf-8').strip()
                                if line_str.startswith('data: '):
                                    data_str = line_str[6:]
                                    if data_str == '[DONE]':
                                        break
                                    
                                    data_json = json.loads(data_str)
                                    if 'choices' in data_json and len(data_json['choices']) > 0:
                                        choice = data_json['choices'][0]
                                        if 'text' in choice:
                                            yield choice['text']
                            except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as e:
                                logger.warning(f"Error parsing LLM response line: {e}")
                                continue
                                
        except Exception as e:
            logger.error(f"Error connecting to LLM: {e}")
            yield f"Ошибка подключения к LLM: {str(e)}"


# Создаем единственный экземпляр сервиса
llm_service = LLMService()