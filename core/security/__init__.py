# core/security/__init__.py

from functools import lru_cache
from .jwt import JWTAuth
from .crypto import PasswordHasher
from core.config import get_settings


@lru_cache()
def get_jwt() -> JWTAuth:
    settings = get_settings()
    return JWTAuth(
        secret=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )


@lru_cache()
def get_pwd_hasher() -> PasswordHasher:
    return PasswordHasher("argon2")
