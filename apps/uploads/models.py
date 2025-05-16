# apps/uploads/models.py

from sqlmodel import SQLModel, Field
from datetime import datetime
from ulid import ULID

from utils.time import current_time


class Upload(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    file_name: str
    url: str
    content_type: str | None = None
    size: int | None = None
    storage_backend: str = "local"  # local or s3
    md5: str | None = None

    owner_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=current_time)
    updated_at: datetime = Field(default_factory=current_time)
