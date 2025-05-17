# apps/uploads/endpoints.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from apps.auth.deps import active_token
from apps.uploads.schemas import UploadRead
from apps.uploads.services import (
    get_upload_by_id,
    delete_upload_file,
    list_all_uploads,
    list_user_uploads,
)
from apps.uploads.storages import get_storage
from core.database import get_session

router = APIRouter()


# ------------------------------------------
# POST /upload
# Authenticated
# ------------------------------------------
@router.post("/")
async def upload(file: UploadFile = File(...), _=Depends(active_token)):
    storage = get_storage()
    file_name = file.filename
    try:
        # Generate a unique file name
        await storage.upload_file(file, file_name)
        url = storage.get_url(file_name)
        return {"filename": file_name, "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
