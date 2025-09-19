from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings

# Создаем движок для базы данных
engine = create_async_engine(
    settings.db_url.get_secret_value(),
    echo=settings.environment.value == "development"
)

# Создаем фабрику сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии базы данных"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Типизированная зависимость для сессии БД
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
