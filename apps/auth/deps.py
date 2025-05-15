# apps/auth/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.security import get_jwt
from typing import Annotated
from .schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


# ------------------------------------------
# Token Based Dependencies
# Only checks the token and the claims
# ------------------------------------------


async def get_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenPayload:
    """Get the token payload from the JWT token."""
    try:
        jwt_auth = get_jwt()
        data = jwt_auth.decode_token(token, kind="access")
        return TokenPayload(**data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def active_token(payload: TokenPayload = Depends(get_token_payload)):
    if not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def staff_token(payload: TokenPayload = Depends(active_token)):
    if not payload.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff privileges required",
        )
    return payload


async def admin_token(payload: TokenPayload = Depends(staff_token)):
    if not payload.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return payload
