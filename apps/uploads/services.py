# apps/uploads/services.py

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import UploadFile, HTTPException, status

from apps.uploads.models import Upload
from apps.uploads.schemas import UploadRead, UploadCreate
from apps.users.models import User
from apps.uploads.storages import get_storage
from sqlmodel import select
import hashlib

from core.security.jwt import TokenUser


async def save_upload_file(
    file: UploadFile,
    user: User | TokenUser,
    session: AsyncSession,
    public: bool = False,
) -> UploadRead:
    storage = get_storage(public=public)
    file_bytes = await file.read()
    file.file.seek(0)  # rewind for actual upload

    # Compute MD5 hash for integrity check
    md5_hash = hashlib.md5(file_bytes).hexdigest()
    file_name = file.filename

    # Upload to the storage
    uploaded_name = await storage.upload_file(file, file_name)
    file_url = storage.get_url(uploaded_name)

    upload_data = UploadCreate(
        file_name=file_name,
        url=file_url,
        public=public,
        owner_id=user.id,
        content_type=file.content_type,
        size=len(file_bytes),
        storage_backend=storage.__class__.__name__.lower(),
        md5=md5_hash,
    )
    upload = Upload(**upload_data.model_dump())
    session.add(upload)
    await session.commit()
    await session.refresh(upload)
    return UploadRead.model_validate(upload_data)


async def delete_upload_file(
    upload_id: str,
    session: AsyncSession,
) -> bool:
    storage = get_storage()
    upload = await session.get(Upload, upload_id)
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content 'Upload' not found",
        )
    if upload.reference_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete upload with active references",
        )
    await storage.delete_file(upload.file_name)
    await session.delete(upload)
    await session.commit()
    return True


async def list_all_uploads(
    session: AsyncSession,
) -> list[UploadRead]:
    stmt = select(Upload)
    result = await session.exec(stmt)
    return result.all()


async def list_user_uploads(
    user_id: str,
    session: AsyncSession,
) -> list[UploadRead]:
    stmt = select(Upload).where(Upload.owner_id == user_id)
    result = await session.exec(stmt)
    return result.all()


async def get_upload_by_id(
    upload_id: str,
    session: AsyncSession,
) -> UploadRead | None:
    return await session.get(Upload, upload_id)
