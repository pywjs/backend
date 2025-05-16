# apps/cms/schemas/post.py
from typing import Literal

from sqlmodel import SQLModel


class PostBase(SQLModel):
    title: str
    slug: str
    body_field: Literal["json", "html", "markdown"] = "json"  # Default to JSON
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    is_published: bool = False
    # metadata
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: list[str] | None = None
    canonical_url: str | None = None
    robots_directives: str | None = "index, follow"
    og_title: str | None = None
    og_description: str | None = None
    og_image_url: str | None = None
    og_type: str | None = "website"
    structured_data: dict | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    title: str | None = None
    slug: str | None = None
    body_field: Literal["json", "html", "markdown"] | None = None
    body_json: dict | None = None
    body_html: str | None = None
    body_markdown: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    is_published: bool | None = False
    # metadata
    meta_title: str | None = None
    meta_description: str | None = None
    meta_keywords: list[str] | None = None
    canonical_url: str | None = None
    robots_directives: str | None = "index, follow"
    og_title: str | None = None
    og_description: str | None = None
    og_image_url: str | None = None
    og_type: str | None = "website"


class PostRead(PostBase):
    id: str
    created_at: str
    updated_at: str
    published_at: str | None = None

    class Config:
        orm_mode = True
