# apps/auth/services.py

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.auth.exceptions import (
    UserIsDeletedException,
    UserNotFoundException,
    UserNotActiveException,
    InvalidCredentialsException,
)
from apps.users.models import User
from apps.users.services import UserService
from core.security import get_jwt, get_pwd_hasher
from core.security.jwt import TokenPair, TokenUser


class AuthService:
    def __init__(self, session: AsyncSession):
        self.jwt = get_jwt()
        self.pwd_hasher = get_pwd_hasher()
        self.session = session
        self.user_service = UserService(session=self.session)

    async def authenticate(self, email: EmailStr, password: str) -> User | None:
        """Authenticate user by email and password."""
        user = await self.user_service.get_user_by_email(email=email)
        # Check if user exists
        if not user:
            raise UserNotFoundException
        # Check if user is active
        if not user.is_active:
            raise UserNotActiveException
        # Check if user is_deleted
        if user.is_deleted:
            raise UserIsDeletedException
        if not self.pwd_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsException
        return user

    async def login(self, email: EmailStr, password: str) -> TokenPair:
        user = await self.authenticate(email=email, password=password)
        email_str = str(user.email)
        token_user = TokenUser(
            id=user.id,
            email=email_str,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_verified=user.is_verified,
            is_admin=user.is_admin,
        )
        return self.jwt.token_pair(token_user)

    async def refresh(self, refresh_token: str) -> TokenPair:
        """Refresh access token using refresh token."""
        try:
            is_valid = self.jwt.verify(token=refresh_token, token_type="refresh")
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token.",
                )
            token_data = self.jwt.token_data(token=refresh_token)
            user = await self.user_service.get_by_id(token_data.id)
            token_user = TokenUser(
                id=user.id,
                email=str(user.email),
                is_active=user.is_active,
                is_staff=user.is_staff,
                is_verified=user.is_verified,
                is_admin=user.is_admin,
            )
            return self.jwt.token_pair(token_user)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )
