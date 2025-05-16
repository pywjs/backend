# apps/cms/schemas/page.py
from sqlmodel import SQLModel
from ulid import ULID
from .base import (
    BaseContentSchema,
    BaseContentUpdateSchema,
    BaseMetadataSchema,
    BaseTimestampSchema,
)


class PageCreate(SQLModel, BaseContentSchema, BaseMetadataSchema, BaseTimestampSchema):
    pass


class PageUpdate(
    SQLModel, BaseContentUpdateSchema, BaseMetadataSchema, BaseTimestampSchema
):
    pass


class PageRead(PageCreate):
    id: str | ULID | None = None
