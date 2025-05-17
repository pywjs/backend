# apps/uploads/storages/s3.py

import aioboto3
from apps.uploads.storages.base import BaseStorage
from fastapi import UploadFile

from core.config import get_settings


class S3Storage(BaseStorage):
    def __init__(self, public: bool = False):
        self.public = public
        self._settings = get_settings()
        self.bucket_name = self._settings.S3_BUCKET_NAME
        self.s3_client_kwargs = {
            "service_name": "s3",
            "aws_access_key_id": self._settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": self._settings.AWS_SECRET_ACCESS_KEY,
            "endpoint_url": self._settings.S3_ENDPOINT_URL,
        }
        if self._settings.S3_REGION_NAME:
            self.s3_client_kwargs["region_name"] = self._settings.S3_REGION_NAME

    async def upload_file(self, file: UploadFile, file_name: str) -> str:
        session = aioboto3.Session()
        _extra_args = {"ACL": "public-read"} if self.public else {}
        async with session.client(**self.s3_client_kwargs) as s3:
            await s3.upload_fileobj(
                file.file, self.bucket_name, file_name, ExtraArgs=_extra_args
            )
        return file_name

    async def delete_file(self, file_name: str) -> None:
        session = aioboto3.Session()
        async with session.client(**self.s3_client_kwargs) as s3:
            await s3.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_url(self, file_name: str) -> str:
        settings = get_settings()
        return f"{settings.S3_ENDPOINT_URL}/{self.bucket_name}/{file_name}"
