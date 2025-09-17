from fastapi import FastAPI
from fastapi.responses import JSONResponse


# Создание FastAPI приложения
app = FastAPI(
    title="Counselor API",
    description="Backend для проекта Counselor",
    version="1.0.0"
)

# Подключение роутеров
# app.include_router(main_router)

# Простейший роутер с приветствием
@app.get("/")
async def root():
    """
    Главная страница с приветствием
    """
    return {"message": "Привет! Добро пожаловать в Counselor API"}
