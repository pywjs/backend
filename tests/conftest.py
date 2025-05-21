# tests/conftest.py
from httpx import AsyncClient, ASGITransport
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from core.security import get_pwd_hasher, get_jwt
from core.security.jwt import TokenUser, TokenPair, VerificationToken
from main import app
from core.database import get_session
from sqlmodel import SQLModel
import asyncio
from unittest.mock import AsyncMock
from core.config import Settings
from apps.users.models import User

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


@pytest.fixture(scope="function", autouse=True)
def patch_settings(monkeypatch):
    mock_settings = Settings(
        DATABASE_URL="sqlite+aiosqlite:///:memory:",
        SECRET_KEY="test-secret",
        ADMIN_EMAIL="test@example.com",  # type: ignore
        ADMIN_PASSWORD="test123",
        SMTP_HOST="smtp.test.local",
        SMTP_PORT=587,
        SMTP_FROM="Test <test@example.com>",
    )
    monkeypatch.setattr("core.config.get_settings", lambda: mock_settings)


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


# ----------------------------------
# Patch email sending
# ----------------------------------
@pytest.fixture(autouse=True)
def mock_send_verification_email(monkeypatch):
    """Mock the send_verification_email function globally."""
    monkeypatch.setattr("utils.email.send_verification_email", AsyncMock())


# ----------------------------------
# Users
# ----------------------------------
@pytest.fixture
async def create_test_user(setup_database, client: AsyncClient) -> User | None:
    async for session in override_get_session():
        password = "test123"
        user = User(
            email="test@example.com",
            hashed_password=get_pwd_hasher().hash(password),
            is_active=True,
            is_staff=False,
            is_admin=False,
            is_verified=True,
            is_deleted=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    return None


@pytest.fixture
async def create_inactive_user(create_test_user: User) -> User | None:
    create_test_user.email = "inactive@example.com"  # type: ignore
    create_test_user.is_active = False
    await save_user_to_db(create_test_user)
    return create_test_user


@pytest.fixture
async def create_deleted_user(create_test_user: User) -> User | None:
    create_test_user.email = "deleted@example.com"  # type: ignore
    create_test_user.is_deleted = True
    await save_user_to_db(create_test_user)
    return create_test_user


@pytest.fixture
async def create_staff_user(create_test_user: User) -> User | None:
    create_test_user.email = "staff@example.com"  # type: ignore
    create_test_user.is_staff = True
    await save_user_to_db(create_test_user)
    return create_test_user


@pytest.fixture
async def create_admin_user(create_test_user: User) -> User | None:
    create_test_user.email = "admin@example.com"  # type: ignore
    create_test_user.is_admin = True
    await save_user_to_db(create_test_user)
    return create_test_user


async def save_to_db(instance: SQLModel) -> None:
    async for session in override_get_session():
        session.add(instance)
        await session.commit()
        await session.refresh(instance)


async def save_user_to_db(user: User) -> None:
    async for session in override_get_session():
        session.add(user)
        await session.commit()
        await session.refresh(user)


# ----------------------------------
# Token
# ----------------------------------
@pytest.fixture
async def get_token_pair_for_user() -> callable:
    jwt = get_jwt()

    async def _token_pair(user: User) -> TokenPair:
        token_user = TokenUser(
            id=user.id,
            email=str(user.email),
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_verified=user.is_verified,
        )
        return jwt.token_pair(token_user)

    return _token_pair


@pytest.fixture
async def get_verification_token_for_user() -> callable:
    jwt = get_jwt()

    async def _verification_token(user: User) -> VerificationToken:
        token_user = TokenUser(
            id=user.id,
            email=str(user.email),
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_verified=user.is_verified,
        )
        return jwt.verification_token(token_user)

    return _verification_token
