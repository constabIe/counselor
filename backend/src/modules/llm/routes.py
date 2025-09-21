from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import logging

from .websocket import websocket_chat_handler
from src.storages.sql.dependencies import get_db_session
from src.modules.users import repository as user_repo
from src.utils.security import verify_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ws-info")
async def websocket_info():
    """
    Информация о подключении к WebSocket чату
    """
    return {
        "endpoint": "/chat/ws/chat/{user_id}",
        "auth_method": "JWT token in query parameter",
        "example": "ws://localhost:8000/chat/ws/chat/your-user-id?token=your-jwt-token",
        "message_format": {
            "message": "Your message text",
            "timestamp": "ISO format timestamp"
        },
        "response_types": [
            "user_message - confirmation",
            "ai_chunk - streaming response chunks", 
            "ai_complete - final response",
            "error - error messages"
        ]
    }


async def authenticate_websocket_user(token: str, session: AsyncSession):
    """Аутентификация пользователя для WebSocket"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required"
        )
    
    # Проверяем токен
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Получаем пользователя из БД
    user = await user_repo.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


@router.websocket("/ws/chat/{user_id}")
async def websocket_chat(
    websocket: WebSocket, 
    user_id: str,
    token: Optional[str] = Query(None)
):
    """
    WebSocket endpoint для чата с AI помощником
    Требует токен аутентификации в query параметре: ?token=your_jwt_token
    """
    # Получаем сессию БД
    async for session in get_db_session():
        try:
            # Аутентифицируем пользователя
            if not token:
                await websocket.close(code=1008, reason="Token required")
                return
                
            authenticated_user = await authenticate_websocket_user(token, session)
            
            # Проверяем, что user_id совпадает с аутентифицированным пользователем
            if str(authenticated_user.id) != str(user_id):
                await websocket.close(code=1008, reason="User ID mismatch")
                return
            
            logger.info(f"User {authenticated_user.id} authenticated for WebSocket chat")
            
            # Запускаем обработчик WebSocket
            await websocket_chat_handler(websocket, authenticated_user.id)
            
        except HTTPException as e:
            logger.warning(f"WebSocket authentication failed: {e.detail}")
            await websocket.close(code=1008, reason=e.detail)
        except Exception as e:
            logger.error(f"WebSocket authentication error: {str(e)}")
            await websocket.close(code=1011, reason="Authentication error")
        finally:
            break  # Выходим из цикла async for