# apps/cms/schemas/base.py
from datetime import datetime
from typing import Literal

from sqlmodel import Field
from pydantic import HttpUrl, field_serializer
from core.schemas import RequestSchema, ResponseSchema, SlugRequest, PublishableRequest


class BaseContentSchema(RequestSchema):
    # For create requests
    title: str
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] = "json"
    # SlugMixin
    slug: str
    # PublishableMixin
    is_published: bool = False
    published_at: datetime | None = None


class BaseContentRequest(SlugRequest, PublishableRequest, RequestSchema):
    title: str
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] = "json"


class BaseContentUpdateSchema(RequestSchema):
    # For update requests
    title: str | None = None
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] | None = None
    # SlugMixin
    slug: str | None = None
    # PublishableMixin
    is_published: bool | None = None


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


class BaseTimestampSchema(ResponseSchema):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    published_at: datetime | None = None
