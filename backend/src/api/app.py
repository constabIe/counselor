from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.modules.landing.routes import router as landing_router
from src.modules.users.routes import router as users_router
from src.modules.cv.routes import router as cv_router
from src.modules.courses.routes import router as courses_router
from src.modules.generation.routes import router as generation_router
from src.modules.jobs.routes import router as jobs_router
from src.modules.folders.routes import router as folders_router
from src.modules.badges.router import router as badges_router

# Создание FastAPI приложения
app = FastAPI(
    title="HR Counselor API",
    description="Backend для HR помощника с поддержкой ИИ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.cors_allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(landing_router)
app.include_router(users_router)
app.include_router(cv_router)
app.include_router(courses_router)
app.include_router(generation_router)
app.include_router(jobs_router)
app.include_router(folders_router)
app.include_router(badges_router)

# Health check endpoint
@app.get("/health", tags=["system"])
def health_check():
    """
    Проверка состояния API
    """
    return {"status": "ok", "message": "HR Counselor API is running"}
