# apps/uploads/storages/s3.py

import aioboto3
from apps.uploads.storages.base import BaseStorage
from fastapi import UploadFile

from core.config import get_settings


class S3Storage(BaseStorage):
    settings = get_settings()
    bucket_name = settings.S3_BUCKET_NAME
    s3_client_kwargs = {
        "service_name": "s3",
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "endpoint_url": settings.S3_ENDPOINT_URL,
    }
    if settings.S3_REGION_NAME:
        s3_client_kwargs["region_name"] = settings.S3_REGION_NAME

    async def upload_file(self, file: UploadFile, file_name: str) -> str:
        session = aioboto3.Session()
        async with session.client(**self.s3_client_kwargs) as s3:
            await s3.upload_fileobj(file.file, self.bucket_name, file_name)
        return file_name

    async def delete_file(self, file_name: str) -> None:
        session = aioboto3.Session()
        async with session.client(**self.s3_client_kwargs) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_url(self, file_name: str) -> str:
        settings = get_settings()
        return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{file_name}"
