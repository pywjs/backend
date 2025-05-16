# apps/cms/schemas/base.py
from typing import Literal

from sqlmodel import SQLModel
from pydantic import HttpUrl


class BaseContentSchema(SQLModel):
    title: str
    slug: str
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: Literal["json", "html", "markdown"] = "json"
    is_published: bool = False


class BaseMetadataSchema(SQLModel):
    # SEO fields
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: list[str] | None = None
    canonical_url: HttpUrl | None = None
    robots_directives: str | None = "index, follow"
    og_title: str | None = None
    og_description: str | None = None
    og_image_url: HttpUrl | None = None
    og_type: str | None = "website"
    structured_data: dict | None = None
