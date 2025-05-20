# apps/uploads/storages/local.py
from pathlib import Path
from fastapi import UploadFile

from apps.uploads.storages.base import BaseStorage
from core.config import get_settings


class LocalFileStorage(BaseStorage):
    def __init__(self, public: bool = False):
        self.public = public
        self._settings = get_settings()
        self.uploads_root = Path(self._settings.UPLOADS_ROOT)
        # Ensure the uploads directory exists
        self.uploads_root.mkdir(parents=True, exist_ok=True)
        self.uploads_url = self._settings.UPLOADS_URL

    async def upload_file(self, file: UploadFile, file_name: str) -> str:
        file_path = Path(self.uploads_root) / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            while chunk := await file.read(1024):
                f.write(chunk)
        return file_name

    async def delete_file(self, file_name: str) -> None:
        file_path = Path(self.uploads_root) / file_name
        if file_path.exists():
            file_path.unlink()

    def get_url(self, file_name: str) -> str:
        return f"{self.uploads_url}/{file_name}"
