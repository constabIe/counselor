import json
import logging
import uuid
from typing import Dict, Union
from fastapi import WebSocket, WebSocketDisconnect
from .service import llm_service

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[Union[str, uuid.UUID], WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: Union[str, uuid.UUID]):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected to chat")
    
    def disconnect(self, user_id: Union[str, uuid.UUID]):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from chat")
    
    async def send_message(self, user_id: Union[str, uuid.UUID], message: str):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_text(message)

    def is_connected(self, user_id: Union[str, uuid.UUID]) -> bool:
        return user_id in self.active_connections


manager = ConnectionManager()


async def websocket_chat_handler(websocket: WebSocket, user_id: Union[str, uuid.UUID]):
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                
                if not user_message.strip():
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Пустое сообщение"
                    }))
                    continue
                
                # Отправляем подтверждение получения сообщения
                await websocket.send_text(json.dumps({
                    "type": "user_message",
                    "message": user_message
                }))
                
                # Генерируем ответ от LLM
                full_response = ""
                async for chunk in llm_service.generate_response(user_message):
                    full_response += chunk
                    # Отправляем каждый чанк клиенту
                    await websocket.send_text(json.dumps({
                        "type": "ai_chunk",
                        "chunk": chunk
                    }))
                
                # Отправляем сигнал завершения ответа
                await websocket.send_text(json.dumps({
                    "type": "ai_complete",
                    "full_message": full_response
                }))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Неверный формат сообщения"
                }))
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Ошибка обработки: {str(e)}"
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {str(e)}")
        manager.disconnect(user_id)