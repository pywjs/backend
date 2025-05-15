# apps/users/routes/v1.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from ulid import ULID
from apps.auth.deps import staff_token, active_token, admin_token
from apps.users.schemas import UserRead, UserCreate, UserUpdate, UserUpdateMe
from core.database import AsyncSession, get_session
from apps.users.services import (
    create_user,
    get_user_by_id,
    list_users,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/v1/users", tags=["users"])

# ------------------------------------------
# POST /users
# ------------------------------------------


@router.post("/", response_model=UserRead)
async def create_new_user(
    user: UserCreate, session: AsyncSession = Depends(get_session)
):
    try:
        new_user = await create_user(user, session)
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
    _=Depends(staff_token),
):
    users = await list_users(session)
    return users


# ------------------------------------------
# GET /users/me
# Self
# ------------------------------------------


@router.get("/me", response_model=UserRead)
async def read_current_user(
    token=Depends(active_token),
    session: AsyncSession = Depends(get_session),
):
    print(token)
    user = await get_user_by_id(token.sub, session)
    if not user:
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
    token=Depends(active_token),
):
    # Get DB Resource
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check Access
    if not (token.is_staff or user_id == token.user_id):
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
    token=Depends(active_token),
):
    user = await update_user(token.sub, user_update, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
    token=Depends(staff_token),
):
    if not token.is_staff:
        raise HTTPException(
            status_code=403,
            detail="Permission Denied",
        )

    user = await update_user(user_id, user_update, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/me")
async def delete_own_account(
    token=Depends(active_token),
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_id(token.user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
    token=Depends(admin_token),
):
    if not token.is_admin and user_id != token.user_id:
        raise HTTPException(
            status_code=403,
            detail="Permission Denied",
        )
    success = await delete_user(user_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
