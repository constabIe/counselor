from __future__ import annotations

from typing import List, Set, Optional
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.badges import repository as badge_repo
from src.modules.badges.models import UserBadgesResponse, BadgeStatsResponse, UserBadgeResponse, BadgeResponse
from src.modules.cv import repository as cv_repo
from src.modules.courses import enrollment_repository as course_enrollment_repo
from src.modules.users import repository as user_repo
from src.storages.sql.models import Badge, UserBadge, EnrollmentStatus


class BadgeService:
    
    async def check_and_award_badges(self, session: AsyncSession, user_id: UUID, trigger: str, **kwargs):
        """Проверяет и выдает бэйджи по триггеру"""
        
        # Получаем все бэйджи пользователя чтобы не выдавать дубли
        user_badge_codes = await badge_repo.get_user_badge_codes(session, user_id)
        
        # Проверяем условия для каждого типа триггера
        new_badges = []
        
        if trigger == "course_completed":
            new_badges.extend(await self._check_course_badges(session, user_id, user_badge_codes, **kwargs))
            
        elif trigger == "course_enrolled":
            new_badges.extend(await self._check_course_badges(session, user_id, user_badge_codes, **kwargs))
            
        elif trigger == "cv_uploaded":
            new_badges.extend(await self._check_cv_badges(session, user_id, user_badge_codes, **kwargs))
            
        elif trigger == "profile_updated":
            new_badges.extend(await self._check_profile_badges(session, user_id, user_badge_codes, **kwargs))
            # Также проверяем CV бейджи при обновлении профиля
            new_badges.extend(await self._check_cv_badges(session, user_id, user_badge_codes, **kwargs))
            
        elif trigger == "user_registered":
            new_badges.extend(await self._check_registration_badges(session, user_id, user_badge_codes, **kwargs))
        
        # Выдаем новые бэйджи
        awarded_badges = []
        for badge_code in new_badges:
            badge = await self.award_badge(session, user_id, badge_code)
            if badge:
                awarded_badges.append(badge)
        
        return awarded_badges
    
    async def _check_course_badges(self, session: AsyncSession, user_id: UUID, user_badges: Set[str], **kwargs) -> List[str]:
        """Проверяет бэйджи связанные с курсами"""
        new_badges = []
        
        # Получаем количество записей на курсы
        total_enrollments = await course_enrollment_repo.count_user_enrollments(session, user_id)
        
        # Получаем статистику по статусам
        enrollment_stats = await course_enrollment_repo.get_enrollment_counts_by_status(session, user_id)
        completed_count = enrollment_stats.get("completed", 0)
        
        # Первый курс (запись на курс)
        if "first_course" not in user_badges and total_enrollments >= 1:
            new_badges.append("first_course")
        
        # Быстрый ученик (запись на 3 курса)
        if "fast_learner" not in user_badges and total_enrollments >= 3:
            new_badges.append("fast_learner")
            
        # Добавим новый бейдж для завершения курса
        if "course_master" not in user_badges and completed_count >= 1:
            new_badges.append("course_master")
        
        return new_badges

    async def _check_cv_badges(self, session: AsyncSession, user_id: UUID, user_badges: Set[str], **kwargs) -> List[str]:
        """Проверяет бэйджи связанные с CV"""
        new_badges = []
        
        # Первое CV
        if "first_cv" not in user_badges:
            cv_count = await cv_repo.get_user_active_cv_count(session, user_id)
            if cv_count >= 1:
                new_badges.append("first_cv")
        
        # Оптимизатор CV - за обновление полей CV (используем kwargs для передачи информации)
        if "cv_optimizer" not in user_badges:
            update_count = kwargs.get("cv_update_count", 0)
            if update_count >= 5:  # После 5 обновлений CV
                new_badges.append("cv_optimizer")
        
        return new_badges
    
    async def _check_profile_badges(self, session: AsyncSession, user_id: UUID, user_badges: Set[str], **kwargs) -> List[str]:
        """Проверяет бэйджи связанные с профилем"""
        new_badges = []
        
        # Мастер профиля - проверяем количество CV пользователя
        if "profile_master" not in user_badges:
            cv_count = await cv_repo.get_user_active_cv_count(session, user_id)
            if cv_count >= 3:  # Если у пользователя есть 3+ активных CV
                new_badges.append("profile_master")
        
        return new_badges
    
    async def _check_registration_badges(self, session: AsyncSession, user_id: UUID, user_badges: Set[str], **kwargs) -> List[str]:
        """Проверяет бэйджи при регистрации"""
        new_badges = []
        
        # Ранняя пташка - заполнил профиль в первый день
        if "early_bird" not in user_badges:
            # Пока просто выдаем всем новым пользователям
            new_badges.append("early_bird")
        
        return new_badges

    async def award_badge(self, session: AsyncSession, user_id: UUID, badge_code: str) -> Optional[UserBadge]:
        """Выдает бэйдж пользователю"""
        
        # Проверяем, есть ли уже такой бэйдж у пользователя
        if await badge_repo.user_has_badge(session, user_id, badge_code):
            return None
        
        # Получаем бэйдж по коду
        badge = await badge_repo.get_badge_by_code(session, badge_code)
        if not badge:
            return None
        
        # Создаем связь
        user_badge = await badge_repo.create_user_badge(session, user_id, badge.id)
        
        # Начисляем XP пользователю
        await user_repo.add_xp_to_user(session, user_id, badge.xp_reward)
        
        return user_badge

    async def get_user_badges(self, session: AsyncSession, user_id: UUID) -> UserBadgesResponse:
        """Получает все бэйджи пользователя"""
        
        user_badges = await badge_repo.get_user_badges(session, user_id)
        stats = await badge_repo.get_user_badge_stats(session, user_id)
        
        # Получаем информацию о бэйджах для каждого UserBadge
        badge_responses = []
        for user_badge in user_badges:
            # Получаем бэйдж по ID через дополнительный запрос
            badge_result = await session.execute(
                select(Badge).where(Badge.id == user_badge.badge_id)  # type: ignore
            )
            badge = badge_result.scalar_one_or_none()
            
            if badge:
                badge_response = BadgeResponse.from_orm(badge)
                user_badge_response = UserBadgeResponse(
                    badge=badge_response,
                    earned_at=user_badge.earned_at
                )
                badge_responses.append(user_badge_response)
        
        return UserBadgesResponse(
            badges=badge_responses,
            total_count=stats["earned_badges"],
            total_xp=stats["total_xp_from_badges"],
            by_category=stats["by_category"]
        )

    async def get_all_badges(self, session: AsyncSession) -> List[BadgeResponse]:
        """Получает все доступные бэйджи"""
        badges = await badge_repo.get_all_badges(session)
        return [BadgeResponse.from_orm(badge) for badge in badges]

    async def get_user_badge_stats(self, session: AsyncSession, user_id: UUID) -> BadgeStatsResponse:
        """Получает статистику бэйджей пользователя"""
        stats = await badge_repo.get_user_badge_stats(session, user_id)
        return BadgeStatsResponse(**stats)


# Создаем экземпляр сервиса
badge_service = BadgeService()
