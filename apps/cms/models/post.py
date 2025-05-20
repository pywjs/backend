# apps/cms/models/post.py
from .base import BasePost
from sqlalchemy import JSON
from sqlmodel import Field


class Post(BasePost, table=True):
    category: str | None = None
    tags: list[str] | None = Field(default=None, sa_type=JSON)
