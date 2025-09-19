from __future__ import annotations

from enum import StrEnum
import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import BaseModel


def utcnow() -> datetime:
    return datetime.utcnow()


class UserRole(StrEnum):
    USER = "user"
    HR = "hr"
    ADMIN = "admin"


class Base(SQLModel):
    pass


class User(Base, table=True):
    __tablename__ = "users"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, max_length=255, unique=True)
    password_hash: str = Field(max_length=255)
    full_name: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class RefreshToken(Base, table=True):
    __tablename__ = "refresh_tokens"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    token: str = Field(index=True, max_length=255)
    expires_at: datetime
    created_at: datetime = Field(default_factory=utcnow)
    is_active: bool = Field(default=True)


class CV(Base, table=True):
    __tablename__ = "cvs"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int = Field(description="Размер файла в байтах")
    content_type: str = Field(max_length=100, default="application/pdf")
    uploaded_at: datetime = Field(default_factory=utcnow)
    is_active: bool = Field(default=True)
    
    # Поля для анализа CV (заполняются ИИ)
    parsed_text: Optional[str] = Field(default=None, description="Извлеченный текст из PDF")
    skills: Optional[str] = Field(default=None, description="Навыки в JSON формате")
    experience_years: Optional[int] = Field(default=None, description="Количество лет опыта")
    education: Optional[str] = Field(default=None, description="Образование в JSON формате")
    analysis_status: str = Field(default="pending", description="Статус анализа: pending, processing, completed, failed")
