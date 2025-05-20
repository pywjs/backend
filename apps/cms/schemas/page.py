# apps/cms/schemas/page.py
from ulid import ULID
from .base import (
    BaseContentSchema,
    BaseContentUpdateSchema,
    BaseMetadataSchema,
    BaseTimestampSchema,
)


class PageCreate(BaseContentSchema, BaseMetadataSchema, BaseTimestampSchema):
    pass


class PageUpdate(BaseContentUpdateSchema, BaseMetadataSchema, BaseTimestampSchema):
    pass


class PageRead(PageCreate):
    id: str | ULID | None = None
