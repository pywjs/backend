# apps/users/endpoints.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from ulid import ULID
from sqlmodel.ext.asyncio.session import AsyncSession
from apps.auth.services import AuthService
from apps.auth.deps import (
    staff_user_token,
    active_user_token,
    admin_user_token,
    active_user,
)
from apps.users.models import User
from apps.users.schemas import UserRead, UserCreate, UserUpdate, UserUpdateMe
from core.database import get_session
from apps.users.services import (
    UserService,
)
from core.security.jwt import TokenUser
from utils.email import send_verification_email

router = APIRouter(tags=["users"])


# ------------------------------------------
# POST /users
# ------------------------------------------
@router.post("/", response_model=UserRead)
async def create_new_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    try:
        auth_service = AuthService(session=session)
        new_user = await auth_service.user_service.create_user(user)
        varification_token = auth_service.jwt.verification_token(new_user)
        background_tasks.add_task(
            send_verification_email,
            str(new_user.email),
            varification_token.code,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return new_user


# ------------------------------------------
# GET /users
# Require: Staff
# ------------------------------------------
@router.get("/", response_model=List[UserRead])
async def read_users(
    session: AsyncSession = Depends(get_session),
    _=Depends(staff_user_token),
):
    user_service = UserService(session=session)
    return await user_service.get_all()


# ------------------------------------------
# GET /users/me
# Self
# ------------------------------------------
@router.get("/me", response_model=UserRead)
async def read_current_user(
    token_user: TokenUser = Depends(active_user_token),
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session=session)
    user = await user_service.get_by_id(token_user.id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------------------------------
# GET /users/{user_id}
# Self | Staff
# ------------------------------------------
@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: ULID,
    session: AsyncSession = Depends(get_session),
    token_user: TokenUser = Depends(active_user_token),
):
    user: User = await active_user(session, token_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check Access
    if user.id != user_id and not user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this user",
        )

    return user


# ------------------------------------------
# PATCH /users/me
# Me
# ------------------------------------------
@router.patch("/me", response_model=UserRead)
async def update_current_user(
    user_update: UserUpdateMe,
    session: AsyncSession = Depends(get_session),
    token_user: TokenUser = Depends(active_user_token),
):
    user_service = UserService(session=session)
    user = await user_service.update_by_id(
        token_user.id, user_update.model_dump(exclude_unset=True)
    )
    return user


# ------------------------------------------
# PATCH /users/{user_id}
# Staff
# ------------------------------------------
@router.patch("/{user_id}", response_model=UserRead)
async def update_existing_user(
    user_id: ULID,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session),
    token_user: TokenUser = Depends(staff_user_token),
):
    if not token_user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="Permission Denied",
        )

    user_service = UserService(session=session)
    user = await user_service.update_by_id(
        str(user_id), user_update.model_dump(exclude_unset=True)
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/me")
async def delete_own_account(
    token_user: TokenUser = Depends(active_user_token),
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session=session)
    user = await user_service.get_by_id(token_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="Staff accounts cannot be deleted",
        )
    # Soft delete
    user.is_deleted = True
    session.add(user)
    await session.commit()
    return {"detail": "Account deleted successfully"}


# ------------------------------------------
# DELETE /users/{user_id}
# Admin
# ------------------------------------------
@router.delete("/{user_id}")
async def delete_existing_user(
    user_id: ULID,
    session: AsyncSession = Depends(get_session),
    token_user: TokenUser = Depends(admin_user_token),
):
    # Only Staff or Admin can delete users
    if not token_user.is_admin and user_id != token_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="Permission Denied",
        )
    user_service = UserService(session=session)
    user = await user_service.delete_by_id(str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
