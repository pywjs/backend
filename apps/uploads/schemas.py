# apps/uploads/schemas.py

from datetime import datetime
from sqlmodel import SQLModel
from pydantic import HttpUrl
from typing import Optional, Literal


class UploadBase(SQLModel):
    file_name: str
    url: HttpUrl | str
    reference_count: int = 0
    public: bool = False
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    storage_backend: Literal["local", "s3"] = "local"
    md5: Optional[str] = None
    owner_id: str


class UploadCreate(UploadBase):
    pass


class UploadRead(UploadBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UploadUpdate(UploadBase):
    title: str | None = None
    description: str | None = None
    public: bool | None = None
