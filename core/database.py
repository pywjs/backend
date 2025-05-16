# core/database.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator


# ------------------------------------------
# Database Models Registration
# Import all models !BEFORE! importing SQLModel to ensure that they are registered
# ------------------------------------------
from apps.users import models as users  # noqa: F401
from sqlmodel import SQLModel  # noqa: F401


# Lazy async_engine builder
def get_async_engine():
    from core.config import get_settings

    settings = get_settings()
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
    )


# Lazy async_sessionmaker
def get_async_sessionmaker():
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Dependency for FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_async_sessionmaker()
    async with async_session() as session:
        yield session
