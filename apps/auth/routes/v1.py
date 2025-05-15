# apps/auth/routes/v1.py

from fastapi import APIRouter
from apps.auth.schemas import TokenResponse, TokenPayload
from fastapi import Depends, HTTPException, status
from apps.auth.schemas import RefreshTokenRequest
from fastapi.security import OAuth2PasswordRequestForm
from core.database import AsyncSession, get_session
from apps.users.services import (
    authenticate_user,
)

from apps.users.schemas import UserLogin
from core.security import get_jwt

router = APIRouter(prefix="/v1/auth", tags=["auth"])

# ------------------------------------------
# POST /auth/token
# OAuth 2.0 Password Flow
# Use Form(...) / application/x-www-form-urlencoded
# ------------------------------------------


@router.post("/token", response_model=TokenResponse)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt = get_jwt()
    return TokenResponse(
        access_token=jwt.create_access_token(
            str(user.id),
            extra={
                "user_email": user.email,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_admin": user.is_admin,
            },
        ),
        refresh_token=jwt.create_refresh_token(str(user.email)),
        token_type="bearer",
    )


# ------------------------------------------
# POST /auth/login
# OAuth 2.0 Password Flow
# Use JSON / application/json
# ------------------------------------------


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(credentials.email, credentials.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt = get_jwt()
    return TokenResponse(
        access_token=jwt.create_access_token(
            str(user.id),
            extra={
                "user_email": user.email,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_admin": user.is_admin,
            },
        ),
        refresh_token=jwt.create_refresh_token(str(user.id)),
        token_type="bearer",
    )


# ------------------------------------------
# POST /auth/refresh
# Refresh access token using refresh token
# ------------------------------------------


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest):
    jwt = get_jwt()

    try:
        data = jwt.decode_token(data.refresh_token, kind="refresh")
        payload = TokenPayload(**data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e

    return TokenResponse(
        access_token=jwt.create_access_token(str(payload.sub)),
        refresh_token=jwt.create_refresh_token(str(payload.sub)),
        token_type="bearer",
    )
