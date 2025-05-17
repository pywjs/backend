# apps/uploads/endpoints.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from apps.auth.deps import active_token
from apps.uploads.schemas import UploadRead
from apps.uploads.services import (
    get_upload_by_id,
    delete_upload_file,
    list_all_uploads,
    list_user_uploads,
    save_upload_file,
)
from core.database import get_session

router = APIRouter()


# ------------------------------------------
# POST /upload
# Authenticated
# ------------------------------------------
@router.post("/")
async def upload(
    file: UploadFile = File(...),
    public: bool = False,
    user=Depends(active_token),
    session=Depends(get_session),
):
    return await save_upload_file(file, user, session, public)


@router.get("/", response_model=list[UploadRead])
async def list_all(
    user=Depends(active_token),
    session=Depends(get_session),
):
    result = []
    """List all uploads for the authenticated user."""
    if user.is_staff:
        result = await list_all_uploads(session=session)
    # If the user is not staff, return only their uploads
    else:
        result = await list_user_uploads(user.id, session=session)
    return result


@router.delete("/{upload_id}", status_code=204)
async def delete_upload(
    upload_id: str,
    user=Depends(active_token),
    session=Depends(get_session),
):
    upload = await get_upload_by_id(upload_id, session=session)
    if not upload:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )
    if upload.owner_id != user.id and not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="User has no permission to delete this file",
        )
    await delete_upload_file(upload.id, session=session)
    return None
