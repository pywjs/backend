# apps/cms/models/navigation.py
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from ulid import ULID


class Navigation(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    name: str  # e.g. "main", "footer", "sidebar"
    slug: str  # e.g. "main-navigation"
    is_active: bool = True  # Is this navigation active?

    items: list["NavigationItem"] = Relationship(back_populates="navigation")


class NavigationItem(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    title: str
    slug: str
    order: int = 0
    is_visible: bool = True
    is_external: bool = False

    # Link targets
    page_id: str | None = Field(default=None, foreign_key="page.id")
    external_url: str | None = None

    # Link to Navigation (many-to-one)
    navigation_id: str = Field(foreign_key="navigation.id")
    navigation: Optional["Navigation"] = Relationship(back_populates="items")

    # Self-referencing nesting
    # noinspection SpellCheckingInspection
    parent_id: str | None = Field(default=None, foreign_key="navigationitem.id")
    parent: Optional["NavigationItem"] = Relationship(back_populates="children")
    children: list["NavigationItem"] = Relationship(back_populates="parent")
