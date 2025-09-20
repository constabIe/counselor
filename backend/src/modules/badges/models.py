from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import List, Dict

from pydantic import BaseModel

from src.storages.sql.models import BadgeCategory


class BadgeResponse(BaseModel):
    id: UUID
    code: str
    name: str
    category: BadgeCategory
    xp_reward: int

    class Config:
        from_attributes = True


class UserBadgeResponse(BaseModel):
    badge: BadgeResponse
    earned_at: datetime

    class Config:
        from_attributes = True


class UserBadgesResponse(BaseModel):
    badges: List[UserBadgeResponse]
    total_count: int
    total_xp: int
    by_category: Dict[str, int]  # количество по категориям


class BadgeStatsResponse(BaseModel):
    earned_badges: int
    total_badges: int
    completion_percentage: float
    total_xp_from_badges: int


class BadgeCreate(BaseModel):
    code: str
    name: str
    category: BadgeCategory
    xp_reward: int = 10
