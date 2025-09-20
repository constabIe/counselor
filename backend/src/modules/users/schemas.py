from __future__ import annotations

from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.storages.sql.models import UserRole


class UserRegisterIn(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, description="Пароль (минимум 6 символов)")
    full_name: str = Field(..., min_length=2, max_length=255, description="Полное имя")
    role: UserRole = Field(default=UserRole.USER, description="Роль пользователя")


class UserLoginIn(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., description="Пароль")


class UserOut(BaseModel):
    id: UUID = Field(..., description="ID пользователя")
    email: str = Field(..., description="Email пользователя")
    full_name: str = Field(..., description="Полное имя")
    role: UserRole = Field(..., description="Роль пользователя")
    is_active: bool = Field(..., description="Активен ли пользователь")
    xp: int = Field(..., description="Количество XP пользователя")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")
    user: UserOut = Field(..., description="Информация о пользователе")


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None


class RatingPercentileResponse(BaseModel):
    percentile: Optional[float] = Field(..., description="Процент пользователей с более низким рейтингом (0-100)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "percentile": 85.5
            }
        }


class UserXPResponse(BaseModel):
    current_xp: int = Field(..., description="Текущее количество XP")
    xp_from_badges: int = Field(..., description="XP от бейджей")
    xp_from_activities: int = Field(..., description="XP от активностей")
    total_earned: int = Field(..., description="Всего заработано XP")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_xp": 150,
                "xp_from_badges": 80,
                "xp_from_activities": 70,
                "total_earned": 150
            }
        }
