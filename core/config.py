# core/config.py
from email.utils import parseaddr

from functools import lru_cache
from typing import Literal
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from pydantic import BeforeValidator


# ------------------------------------------
# Validators
# ------------------------------------------


def validate_smtp_from(value: str) -> str:
    name, email = parseaddr(value)
    if not email or "@" not in email:
        raise ValueError(f"Invalid SMTP_FROM format: {value}")
    return value


# ------------------------------------------
# Settings
# ------------------------------------------


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Storage
    STORAGE_BACKEND: Literal["local", "s3"] = "local"
    # Local storage
    UPLOADS_ROOT: str = "uploads"
    UPLOADS_URL: str = "/uploads"
    # S3 storage
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    S3_REGION_NAME: str | None = None
    S3_BUCKET_NAME: str | None = None
    S3_ENDPOINT_URL: str | None = None

    # Security
    SECRET_KEY: str
    ALGORITHM: Literal["HS256", "HS384", "HS512"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Admin
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str

    # SMTP
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: Annotated[str, BeforeValidator(validate_smtp_from)] = (
        "pywjs backend <noreply@pywjs.com>"
    )
    SMTP_TLS: bool = False
    SMTP_SSL: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
