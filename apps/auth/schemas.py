# apps/auth/schemas.py
from pydantic import EmailStr
from pydantic import Field

from core.schemas import RequestSchema


class LoginRequest(RequestSchema):
    """Request schema for user login."""

    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"email": "user@example.com", "password": "securePassword123"}]
        }
    }


class RefreshTokenRequest(RequestSchema):
    """Request schema for refreshing access token."""

    refresh_token: str
