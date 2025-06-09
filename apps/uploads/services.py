# apps/uploads/services.py

from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import UploadFile, HTTPException, status

from apps.uploads.models import Upload
from apps.uploads.storages import get_storage
from sqlmodel import select
import hashlib

from core.security.jwt import TokenUser
from core.services import BaseService


class UploadService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Upload, session=session)

    async def save_upload_file(
        self,
        file: UploadFile,
        user: TokenUser,
        public: bool = False,
    ) -> Upload:
        storage = get_storage(public=public)
        file_bytes = await file.read()
        file.file.seek(0)

        md5_hash = hashlib.md5(file_bytes).hexdigest()
        file_name = file.filename

        uploaded_name = await storage.upload_file(file, file_name)
        file_url = await storage.get_url(uploaded_name)

        upload = Upload(
            file_name=file_name,
            url=file_url,
            public=public,
            owner_id=user.id,
            content_type=file.content_type,
            size=len(file_bytes),
            storage_backend=storage.name,
            md5=md5_hash,
        )

        self.session.add(upload)
        await self.session.commit()
        await self.session.refresh(upload)
        return upload

    async def delete_upload(self, upload: Upload):
        if upload.reference_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete upload with active references",
            )
        storage = get_storage()
        await storage.delete_file(upload.file_name)
        await self.session.delete(upload)
        await self.session.commit()

    async def get_user_uploads(self, user_id: str) -> list[Upload]:
        stmt = select(self.model).where(self.model.owner_id == user_id)
        result = await self.session.exec(stmt)
        return result.all()

    async def get_upload_with_url(self, upload_id: str) -> Upload:
        upload = await self.get_by_id(upload_id)
        if not upload:
            raise HTTPException(status_code=404, detail="Upload not found")

        storage = get_storage(public=upload.public)
        upload.url = await storage.get_url(upload.file_name)
        return upload
