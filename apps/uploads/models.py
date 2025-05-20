# apps/uploads/models.py

from sqlmodel import Field
from core.models import BaseTable


class Upload(BaseTable, table=True):
    file_name: str
    url: str
    reference_count: int = 0
    public: bool = False

    # metadata fields
    title: str | None = None
    description: str | None = None
    content_type: str | None = None
    size: int | None = None
    storage_backend: str = "local"  # local or s3
    md5: str | None = None

    # foreign key to user
    owner_id: str = Field(foreign_key="user.id", index=True)
