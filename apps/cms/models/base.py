# apps/cms/models/base.py
from sqlalchemy import JSON
from sqlmodel import Field, SQLModel
from core.models import BaseTable, SlugMixin, PublishableMixin


class BaseContent(BaseTable, SlugMixin, PublishableMixin, table=False):
    """Base class for all content models in the CMS."""

    title: str
    body_json: dict | None = Field(default=None, sa_type=JSON)
    body_html: str | None = None
    body_markdown: str | None = None
    body_field: str = "json"  # Default to JSON [json, html, markdown]

    # Computed body property
    @property
    def body(self):
        if self.body_field == "json":
            return self.body_json
        elif self.body_field == "html":
            return self.body_html
        elif self.body_field == "markdown":
            return self.body_markdown
        return None


class BaseMetadata(SQLModel, table=False):
    """Abstract reusable base metadata for Page models."""

    # SEO fields
    meta_title: str | None = None  # SEO title, if different from the page title
    meta_description: str | None = None  # Short description for search engines
    meta_keywords: list[str] | None = Field(
        default=None, sa_type=JSON
    )  # Keywords for search engines
    canonical_url: str | None = (
        None  # Canonical URL to prevent duplicate content issues
    )
    robots_directives: str | None = (
        "index, follow"  # Default to allowing indexing the following links
    )
    og_title: str | None = None  # Open Graph title for social media sharing
    og_description: str | None = None  # Open Graph description for social media sharing
    og_image_url: str | None = None  # URL to image for social media sharing
    og_type: str | None = "website"  # Open Graph content type
    structured_data: dict | None = Field(
        default=None, sa_type=JSON
    )  # JSON-LD structured data for rich snippets


class BasePage(BaseContent, BaseMetadata, table=False):
    pass


class BasePost(BaseContent, BaseMetadata, table=False):
    # Add any additional fields or methods specific to posts here
    pass
