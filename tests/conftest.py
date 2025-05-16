# tests/conftest.py
from httpx import AsyncClient, ASGITransport
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from main import app
from core.database import get_session
from sqlmodel import SQLModel
import asyncio

# ------------------------------------------
# Test settings
# ------------------------------------------

# test database in memory
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Async engine and session for testing
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ----------------------------------
# Override get_session dependency
# ----------------------------------
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


# noinspection PyUnresolvedReferences
app.dependency_overrides[get_session] = override_get_session


# ----------------------------------
# Run once per test session: create schema
# ----------------------------------


# Required for session-level async fixtures
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Run per test to avoid asyncio issues with session-scoped fixtures
@pytest.fixture(scope="function")
async def setup_database():
    """Create tables before tests."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


# ----------------------------------
# Async test client using ASGITransport
# ----------------------------------
@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Async test client using ASGITransport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
