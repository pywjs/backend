# apps/cms/schemas/post.py

from sqlmodel import SQLModel


class PostBase(SQLModel):
    title: str
    slug: str
    body_json: str
    body_html: str
    body_markdown: str
