# apps/auth/endpoints.py

from fastapi import APIRouter, Form
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, BaseModel

from apps.auth.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserIsDeletedException,
    UserNotActiveException,
    InvalidRefreshTokenException,
)
from apps.auth.schemas import LoginRequest
from core.security.exceptions import InvalidTokenException, ExpiredTokenException
from core.security.jwt import TokenPair
from apps.auth.services import AuthService
from core.database import AsyncSession, get_session

router = APIRouter(tags=["auth"])


# ------------------------------------------
# POST /auth/token
# OAuth 2.0 Password Flow
# Use Form(...) / application/x-www-form-urlencoded
# ------------------------------------------
@router.post("/token", response_model=TokenPair)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    # Authenticate user
    email: EmailStr = form_data.username  # type: ignore
    password = form_data.password
    auth_service = AuthService(session=session)
    try:
        return await auth_service.login(email, password)
    except (UserNotFoundException, InvalidCredentialsException, UserIsDeletedException):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotActiveException:
        raise HTTPException(
            status_code=401,
            detail="Account is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ------------------------------------------
# POST /auth/login
# OAuth 2.0 Password Flow
# Use JSON / application/json
# ------------------------------------------
@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Login user with email and password to get access and refresh tokens.
    :param payload: (LoginRequest)
    :param session: AsyncSession
    :return: TokenPair(access_token, refresh_token)
    """
    auth_service = AuthService(session=session)
    try:
        return await auth_service.login(payload.email, payload.password)
    except (UserNotFoundException, InvalidCredentialsException, UserIsDeletedException):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except UserNotActiveException:
        raise HTTPException(status_code=403, detail="Account is not active")


# ------------------------------------------
# POST /auth/refresh
# Refresh access token using refresh token
# Use Form(...) / application/x-www-form-urlencoded
# ------------------------------------------
@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(
    grant_type: str = Form(default="refresh_token"),
    refresh_token: str = Form(...),
    client_id: str | None = Form(default=""),  # noqa
    client_secret: str | None = Form(default=""),  # noqa
    session: AsyncSession = Depends(get_session),
):
    if grant_type and grant_type != "refresh_token":
        raise HTTPException(
            status_code=400,
            detail="Invalid grant_type. Only 'refresh_token' is supported.",
        )
    auth_service = AuthService(session=session)
    try:
        return await auth_service.refresh(refresh_token)
    except InvalidRefreshTokenException:
        raise HTTPException(status_code=401, detail="Invalid refresh token or expired")


# ------------------------------------------
# POST /auth/verify
# Verify email using verification token
# ------------------------------------------
class MessageResponse(BaseModel):
    message: str


@router.get("/verify", response_model=MessageResponse)
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    auth_service = AuthService(session=session)
    try:
        if not auth_service.jwt.verify(token, token_type="verification"):
            raise HTTPException(status_code=401, detail="Invalid verification token")
    except InvalidTokenException:
        raise HTTPException(status_code=401, detail="Invalid verification token")
    except ExpiredTokenException:
        raise HTTPException(status_code=401, detail="Verification token expired")

    data = auth_service.jwt.token_data(token=token)
    user = await auth_service.user_service.get_by_id(data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "Email verified successfully"}
