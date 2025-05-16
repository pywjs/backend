# apps/uploads/backends/__init__.py
from functools import lru_cache

from core.config import get_settings
from .base import BaseStorage


@lru_cache
def get_storage() -> BaseStorage:
    """
    Get the storage backend to use for file uploads.
    """
    settings = get_settings()
    if settings.STORAGE_BACKEND == "s3":
        from apps.uploads.storages.s3 import S3Storage

        return S3Storage()
    elif settings.STORAGE_BACKEND == "local":
        from apps.uploads.storages.local import LocalFileStorage

        return LocalFileStorage()
    else:
        raise ValueError(f"Invalid storage backend: {settings.STORAGE_BACKEND}")
