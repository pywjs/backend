# apps/cms/schemas/post.py
from ulid import ULID
from .base import (
    BaseContentSchema,
    BaseContentUpdateSchema,
    BaseMetadataSchema,
    BaseTimestampSchema,
)


class PostCreate(BaseContentSchema, BaseMetadataSchema, BaseTimestampSchema):
    category: str | None = None
    tags: list[str] | None = None


class PostUpdate(BaseContentUpdateSchema, BaseMetadataSchema, BaseTimestampSchema):
    category: str | None = None
    tags: list[str] | None = None


class PostRead(PostCreate):
    id: str | ULID | None = None
