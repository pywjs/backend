# apps/users/schemas.py
from pydantic import EmailStr, Field
from ulid import ULID
from core.schemas import ResponseSchema, RequestSchema

# Note: Use EmailStr only for the INPUT schemas


class UserCreate(RequestSchema):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str


class UserRead(ResponseSchema):
    """Schema for reading user data."""

    id: ULID
    email: str
    is_active: bool
    is_verified: bool
    is_staff: bool
    is_admin: bool


class UserUpdate(RequestSchema):
    """partial update schema for user data."""

    email: EmailStr | None = Field(None, examples=["jason@gmail.com"])
    password: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    is_staff: bool | None = None


class UserUpdateMe(RequestSchema):
    """Schema for updating the current user's data."""

    email: EmailStr | None = None
    password: str | None = None
