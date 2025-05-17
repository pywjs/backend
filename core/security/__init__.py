# core/security/__init__.py

from functools import lru_cache
from .jwt import JWT
from .crypto import PasswordHasher


@lru_cache()
def get_jwt() -> JWT:
    from core.config import get_settings

    settings = get_settings()
    return JWT(
        secret=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        verification_token_expire_minutes=settings.VERIFICATION_TOKEN_EXPIRE_MINUTES,
    )


@lru_cache()
def get_pwd_hasher() -> PasswordHasher:
    return PasswordHasher("argon2")
