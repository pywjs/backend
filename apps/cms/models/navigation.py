# apps/cms/models/navigation.py
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from ulid import ULID


class Navigation(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    name: str  # e.g. "main, footer, sidebar"
    slug: str  # e.g. "main-navigation"
    is_active: bool = True  # Is this navigation active?

    # Relationship to NavigationItem
    items: list["NavigationItem"] = Relationship(back_populates="navigation")


class NavigationItem(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    title: str
    slug: str
    order: int = 0
    is_visible: bool = True  # Is this item visible?
    is_external: bool = False  # Is this item an external link?

    # Links
    page_id: str | None = Field(
        default=None, foreign_key="page.id"
    )  # ID of the page if internal
    external_url: str | None = None  # URL if external

    # Foreign key to Navigation
    navigation_id: str = Field(foreign_key="navigation.id")
    navigation: Optional["Navigation"] = Relationship(back_populates="items")

    # Optional Nesting
    # noinspection SpellCheckingInspection
    parent_id: str | None = Field(default=None, foreign_key="navigationitem.id")
    parent: Optional["NavigationItem"] = Relationship(back_populates="items")
    children: list["NavigationItem"] = Relationship(back_populates="parent")
