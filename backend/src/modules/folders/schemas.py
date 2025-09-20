from __future__ import annotations

from uuid import UUID
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class FolderCreate(BaseModel):
    name: str = Field(..., max_length=255, description="Название папки")
    description: Optional[str] = Field(None, description="Описание папки")
    job_id: UUID = Field(..., description="ID вакансии, к которой относится папка")


class FolderUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Название папки")
    description: Optional[str] = Field(None, description="Описание папки")


class FolderOut(BaseModel):
    id: UUID = Field(..., description="ID папки")
    name: str = Field(..., description="Название папки")
    description: Optional[str] = Field(..., description="Описание папки")
    job_id: UUID = Field(..., description="ID вакансии")
    created_by: UUID = Field(..., description="Кто создал папку")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    is_active: bool = Field(..., description="Активна ли папка")
    candidates_count: int = Field(0, description="Количество кандидатов в папке")


class FolderList(BaseModel):
    folders: list[FolderOut] = Field(..., description="Список папок")
    total: int = Field(..., description="Общее количество папок")
    page: int = Field(..., description="Текущая страница")
    per_page: int = Field(..., description="Количество элементов на странице")


class CandidateAddToFolder(BaseModel):
    user_id: UUID = Field(..., description="ID кандидата для добавления")
    notes: Optional[str] = Field(None, description="Заметки о кандидате")


class CandidateUpdateInFolder(BaseModel):
    notes: Optional[str] = Field(None, description="Заметки о кандидате")


class FolderCandidateOut(BaseModel):
    id: UUID = Field(..., description="ID записи")
    folder_id: UUID = Field(..., description="ID папки")
    user_id: UUID = Field(..., description="ID кандидата")
    user_full_name: str = Field(..., description="Полное имя кандидата")
    user_email: str = Field(..., description="Email кандидата")
    added_by: UUID = Field(..., description="Кто добавил кандидата")
    added_at: datetime = Field(..., description="Дата добавления")
    notes: Optional[str] = Field(..., description="Заметки о кандидате")
    is_active: bool = Field(..., description="Активна ли запись")


class FolderCandidatesList(BaseModel):
    candidates: list[FolderCandidateOut] = Field(..., description="Список кандидатов в папке")
    total: int = Field(..., description="Общее количество кандидатов")
    page: int = Field(..., description="Текущая страница")
    per_page: int = Field(..., description="Количество элементов на странице")
