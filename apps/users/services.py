# apps/users/services.py

from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from sqlmodel import select
from ulid import ULID
from apps.users.models import User
from apps.users.schemas import UserCreate, UserUpdate, UserUpdateMe
from core.security import get_pwd_hasher

pwd_hasher = get_pwd_hasher()


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    existing_user = await get_user_by_email(user_data.email, session)
    if existing_user:
        raise ValueError("User already exists")

    new_user = User(
        email=user_data.email,
        hashed_password=pwd_hasher.hash(user_data.password),
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(
    email: EmailStr | str, session: AsyncSession
) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.exec(stmt)
    return result.one_or_none()


async def get_user_by_id(user_id: ULID, session: AsyncSession) -> User | None:
    stmt = select(User).where(User.id == str(user_id))
    result = await session.exec(stmt)
    return result.one_or_none()


async def list_users(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result = await session.exec(stmt)
    return result.all()


async def update_user(
    user_id: ULID, user_update: UserUpdate | UserUpdateMe, session: AsyncSession
) -> User | None:
    user = await get_user_by_id(user_id, session)
    if not user:
        return None

    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.hashed_password = pwd_hasher.hash(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(user_id: ULID, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False
    user.is_deleted = True
    session.add(user)
    await session.commit()
    return True


async def hard_delete_user(user_id: ULID, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True


async def authenticate_user(
    email: EmailStr | str, password: str, session: AsyncSession
) -> User | None:
    user = await get_user_by_email(email, session)
    if not user or not pwd_hasher.verify(password, user.hashed_password):
        return None
    return user
