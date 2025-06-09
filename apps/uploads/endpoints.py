# apps/uploads/endpoints.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from core.database import get_session
from core.security.jwt import TokenUser
from apps.auth.deps import active_user_token
from apps.uploads.schemas import UploadRead
from apps.uploads.services import UploadService

router = APIRouter(tags=["uploads"])


def get_upload_service(session=Depends(get_session)) -> UploadService:
    return UploadService(session=session)


@router.post("/", response_model=UploadRead)
async def upload(
    file: UploadFile = File(...),
    public: bool = False,
    token_user: TokenUser = Depends(active_user_token),
    service: UploadService = Depends(get_upload_service),
):
    upload = await service.save_upload_file(file, token_user, public)
    return upload


@router.get("/", response_model=list[UploadRead])
async def list_all(
    token_user: TokenUser = Depends(active_user_token),
    service: UploadService = Depends(get_upload_service),
):
    if token_user.is_staff:
        return await service.get_all()
    return await service.get_user_uploads(token_user.id)


@router.get("/{upload_id}", response_model=UploadRead)
async def get_upload(
    upload_id: str,
    token_user: TokenUser = Depends(active_user_token),
    service: UploadService = Depends(get_upload_service),
):
    upload = await service.get_by_id(upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    if upload.owner_id != token_user.id and not token_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Return the record with refreshed URL
    return await service.get_upload_with_url(upload_id)


@router.delete("/{upload_id}", status_code=204)
async def delete_upload(
    upload_id: str,
    token_user: TokenUser = Depends(active_user_token),
    service: UploadService = Depends(get_upload_service),
):
    upload = await service.get_by_id(upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="File not found")

    if upload.owner_id != token_user.id and not token_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    await service.delete_upload(upload)
    return None
