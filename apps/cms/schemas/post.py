# apps/cms/schemas/post.py
from sqlmodel import SQLModel
from ulid import ULID
from .base import (
    BaseContentSchema,
    BaseContentUpdateSchema,
    BaseMetadataSchema,
    BaseTimestampSchema,
)


class PostCreate(SQLModel, BaseContentSchema, BaseMetadataSchema, BaseTimestampSchema):
    category: str | None = None
    tags: list[str] | None = None


class PostUpdate(
    SQLModel, BaseContentUpdateSchema, BaseMetadataSchema, BaseTimestampSchema
):
    category: str | None = None
    tags: list[str] | None = None


class PostRead(PostCreate):
    id: str | ULID | None = None
