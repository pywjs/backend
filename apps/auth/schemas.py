# apps/auth/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Literal
from ulid import ULID


class RefreshTokenRequest(BaseModel):
    """Request schema for refreshing access token."""

    refresh_token: str


class TokenPayload(BaseModel):
    sub: ULID  # ULID
    iat: int
    exp: int
    iss: str | None = None
    aud: str | None = None
    user_email: EmailStr
    is_active: bool
    is_staff: bool
    is_admin: bool


class TokenResponse(BaseModel):
    """Response schema for token generation."""

    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
