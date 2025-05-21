# apps/cms/schemas/base.py
from typing import Literal

from sqlmodel import Field
from pydantic import HttpUrl, field_serializer, BaseModel

from core.schemas import (
    SlugCreateRequest,
    RequestSchema,
    SlugUpdateRequest,
    SlugResponse,
    ULIDPrimaryKeyResponse,
    TimestampResponse,
    PublishableCreateRequest,
    PublishableUpdateRequest,
    PublishableResponse,
    ResponseSchema,
)
from utils.text import slugify


class BaseContentOptionalsSchema(BaseModel):
    """Fields that are optional for create/update fields."""

    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] = "json"


class BaseContentCreateSchema(
    BaseContentOptionalsSchema,
    SlugCreateRequest,
    PublishableCreateRequest,
    RequestSchema,
):
    title: str

    @field_serializer("slug")
    def serialize_slug(self, v: str) -> str:
        return slugify(v) if v else v


class BaseContentUpdateSchema(
    BaseContentOptionalsSchema,
    SlugUpdateRequest,
    PublishableUpdateRequest,
    RequestSchema,
):
    title: str | None = None

    @field_serializer("slug")
    def serialize_slug(self, v: str) -> str:
        return slugify(v) if v else v


class BaseContentResponse(
    BaseContentOptionalsSchema,
    ULIDPrimaryKeyResponse,
    SlugResponse,
    PublishableResponse,
    TimestampResponse,
    ResponseSchema,
):
    title: str
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] = "json"


class BaseMetadataSchema(RequestSchema):
    # Create/Update requests
    # SEO fields
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: list[str] | None = None
    canonical_url: HttpUrl | None = None
    robots_directives: str | None = Field(default="index, follow")
    og_title: str | None = None
    og_description: str | None = None
    og_image_url: HttpUrl | None = None
    og_type: str | None = Field(default="website")
    structured_data: dict | None = None

    @field_serializer("canonical_url", "og_image_url", when_used="always")
    def serialize_url(self, v: HttpUrl | None) -> str | None:
        if isinstance(v, HttpUrl):
            return str(v)
        return v
