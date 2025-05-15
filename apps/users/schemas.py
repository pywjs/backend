# apps/users/schemas.py

from sqlmodel import SQLModel
from pydantic import EmailStr
from ulid import ULID


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    email: EmailStr
    password: str


class UserRead(SQLModel):
    """Schema for reading user data."""

    id: ULID
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_staff: bool
    is_admin: bool


class UserUpdate(SQLModel):
    """partial update schema for user data."""

    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    is_staff: bool | None = None


class UserUpdateMe(SQLModel):
    """Schema for updating the current user's data."""

    email: EmailStr | None = None
    password: str | None = None


class UserLogin(SQLModel):
    """Schema for user login."""

    email: EmailStr
    password: str
