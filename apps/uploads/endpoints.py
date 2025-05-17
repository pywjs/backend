# apps/uploads/endpoints.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from apps.auth.deps import active_token
from apps.uploads.services import get_upload_by_id, delete_upload_file
from apps.uploads.storages import get_storage
from core.database import get_session

router = APIRouter()


# ------------------------------------------
# POST /upload
# Authenticated
# ------------------------------------------
@router.post("/upload")
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


@router.delete("/delete/{upload_id}", status_code=204)
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
