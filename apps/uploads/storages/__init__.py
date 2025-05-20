# apps/uploads/backends/__init__.py
from functools import lru_cache


from core.config import get_settings
from .base import BaseStorage


@lru_cache
def get_storage(
    *,
    public: bool = False,
) -> BaseStorage:
    """
    Return the correct storage backend configured in settings.
    The `public` flag can be passed for storage backends that treat public/private differently.
    """
    _settings = get_settings()
    _backend = _settings.STORAGE_BACKEND

    if _backend == "s3":
        from apps.uploads.storages.s3 import S3Storage

        return S3Storage(public=public)
    elif _backend == "local":
        from apps.uploads.storages.local import LocalFileStorage

        return LocalFileStorage(public=public)
    else:
        raise ValueError(f"Invalid storage backend: {_backend}")
