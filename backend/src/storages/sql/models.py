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
    xp: int = Field(default=0)


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
    additional_education: Optional[str] = Field(default=None, description="Курсы и сертификаты в JSON формате")
    jobs: Optional[str] = Field(default=None, description="Предыдущие работы в JSON формате")
    current_role: Optional[str] = Field(default=None, description="Текущая роль/должность в JSON формате")
    responsibilities: Optional[str] = Field(default=None, description="Обязанности в текущей роли в JSON формате")
    languages: Optional[str] = Field(default=None, description="Языки в JSON формате")
    age: Optional[int] = Field(default=None, description="Возраст кандидата")
    department: Optional[str] = Field(default=None, description="Подразделение/направление")
    grade: Optional[str] = Field(default=None, description="Грейд (если есть)")
    specialization: Optional[str] = Field(default=None, description="Специализация (например, L1 Support)")
    competencies: Optional[str] = Field(default=None, description="Компетенции с уровнями в JSON формате")
    comments: Optional[str] = Field(default=None, description="Дополнительное описание (свободный текст)")
    rating: Optional[float] = Field(default=None, description="Рейтинг кандидата от ИИ (0-10)")
    tags: Optional[str] = Field(default=None, description="Специальные теги от ИИ в JSON формате")
    career_path: Optional[str] = Field(default=None, description="Предлагаемая карьерная траектория в JSON формате")
    analysis_status: str = Field(default="pending", description="Статус анализа: pending, processing, completed, failed")


class CourseLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(Base, table=True):
    __tablename__ = "courses"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255, description="Название курса")
    direction: str = Field(max_length=255, description="Направление (например, 'IT', 'HR', 'Marketing')")
    level: CourseLevel = Field(description="Уровень сложности курса")
    duration_hours: int = Field(description="Длительность курса в часах")
    description: Optional[str] = Field(default=None, description="Описание курса")
    created_at: datetime = Field(default_factory=utcnow)
    is_active: bool = Field(default=True)


class JobLevel(StrEnum):
    INTERN = "intern"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"


class JobStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    DRAFT = "draft"


class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class Job(Base, table=True):
    __tablename__ = "jobs"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255, description="Название вакансии")
    department: str = Field(max_length=255, description="Отдел/направление")
    level: JobLevel = Field(description="Уровень позиции")
    employment_type: EmploymentType = Field(default=EmploymentType.FULL_TIME, description="Тип занятости")
    location: Optional[str] = Field(default=None, max_length=255, description="Местоположение")
    remote_available: bool = Field(default=False, description="Доступна ли удаленная работа")
    
    # Описание вакансии
    description: str = Field(description="Подробное описание вакансии")
    requirements: str = Field(description="Требования к кандидату")
    responsibilities: str = Field(description="Обязанности")
    
    # Навыки (JSON формат)
    required_skills: Optional[str] = Field(default=None, description="Требуемые навыки в JSON формате")
    
    # Опыт
    min_experience_years: Optional[int] = Field(default=None, description="Минимальный опыт работы в годах")
    max_experience_years: Optional[int] = Field(default=None, description="Максимальный опыт работы в годах")
    
    # Зарплата
    average_salary: Optional[int] = Field(default=None, description="Средняя предлагаемая зарплата")
    salary_currency: str = Field(default="RUB", max_length=10, description="Валюта зарплаты")
    
    # Метаданные
    status: JobStatus = Field(default=JobStatus.DRAFT, description="Статус вакансии")
    created_by: uuid.UUID = Field(foreign_key="users.id", description="Кто создал вакансию")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    published_at: Optional[datetime] = Field(default=None, description="Дата публикации")


class Folder(Base, table=True):
    __tablename__ = "folders"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255, description="Название папки")
    description: Optional[str] = Field(default=None, description="Описание папки")
    job_id: uuid.UUID = Field(foreign_key="jobs.id", description="ID вакансии, к которой относится папка")
    created_by: uuid.UUID = Field(foreign_key="users.id", description="Кто создал папку")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    is_active: bool = Field(default=True, description="Активна ли папка")


class FolderCandidate(Base, table=True):
    __tablename__ = "folder_candidates"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    folder_id: uuid.UUID = Field(foreign_key="folders.id", description="ID папки")
    user_id: uuid.UUID = Field(foreign_key="users.id", description="ID кандидата (пользователя)")
    added_by: uuid.UUID = Field(foreign_key="users.id", description="Кто добавил кандидата в папку")
    added_at: datetime = Field(default_factory=utcnow)
    notes: Optional[str] = Field(default=None, description="Заметки о кандидате")
    is_active: bool = Field(default=True, description="Активна ли запись")


class EnrollmentStatus(StrEnum):
    ENROLLED = "enrolled"      # Записан на курс
    STARTED = "started"        # Начал изучение
    COMPLETED = "completed"    # Завершил курс


class CourseEnrollment(Base, table=True):
    __tablename__ = "course_enrollments"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", description="ID пользователя")
    course_id: uuid.UUID = Field(foreign_key="courses.id", description="ID курса")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.ENROLLED, description="Статус")
    enrolled_at: datetime = Field(default_factory=utcnow, description="Дата записи")
    started_at: Optional[datetime] = Field(default=None, description="Дата начала изучения")
    is_active: bool = Field(default=True)


class BadgeCategory(StrEnum):
    EDUCATION = "education"
    CAREER = "career"
    SKILLS = "skills"
    ACTIVITY = "activity"


class Badge(Base, table=True):
    __tablename__ = "badges"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    code: str = Field(max_length=50, unique=True)
    name: str = Field(max_length=100)
    category: BadgeCategory
    xp_reward: int = Field(default=10)
    created_at: datetime = Field(default_factory=utcnow)


class UserBadge(Base, table=True):
    __tablename__ = "user_badges"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    badge_id: uuid.UUID = Field(foreign_key="badges.id")
    earned_at: datetime = Field(default_factory=utcnow)
