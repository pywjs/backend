# apps/auth/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import get_jwt
from apps.users.models import User
from core.security.exceptions import ExpiredTokenException
from core.security.jwt import TokenUser
from sqlmodel.ext.asyncio.session import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


"""
FastAPI dependencies for authentication and authorization.
They can utilize services, but they are not services themselves,
and they can return HTTPExceptions.
"""


# ------------------------------------------
# Token Based Dependencies
# Only checks the token and the claims
# ------------------------------------------


async def _get_token_data(token: str = Depends(oauth2_scheme)) -> TokenUser:
    """Parse the token and return the payload."""
    try:
        _jwt = get_jwt()
        token_user = _jwt.token_data(token)
        return token_user
    except ExpiredTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def active_user_token(
    token_user: TokenUser = Depends(_get_token_data),
) -> TokenUser:
    """Check if the user is active and also user is not deleted"""
    if not token_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_user


async def staff_user_token(
    token_user: TokenUser = Depends(active_user_token),
) -> TokenUser:
    """Check if the user is staff."""
    if not token_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, PRIVILEGES[S*] required",
        )
    return token_user


async def admin_user_token(
    token_user: TokenUser = Depends(active_user_token),
) -> TokenUser:
    """Check if the user is admin."""
    if not token_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, PRIVILEGES[A*] required",
        )
    return token_user


# ------------------------------------------
# Token + User in DB Helpers
# Cheks the user both in the token and in the DB
# Those are not dependencies. They mean to be used in the endpoints and called directly
#  to separate the services from the database layer.
# ------------------------------------------


async def get_user_or_401(user_id: str, session: AsyncSession) -> User:
    """Get user from DB or raise 401."""
    user_db = await session.get(User, user_id)
    if not user_db or user_db.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # noinspection PyTypeChecker
    return user_db


async def active_user(session: AsyncSession, token_user: TokenUser) -> User:
    """Check if the user is active."""
    return await get_user_or_401(token_user.id, session)


async def staff_user(session: AsyncSession, token_user: TokenUser) -> User:
    """Check if the user is staff."""
    return await get_user_or_401(token_user.id, session)


async def admin_user(session: AsyncSession, token_user: TokenUser) -> User:
    """Check if the user is admin."""
    return await get_user_or_401(token_user.id, session)
