# apps/cms/models/navigation.py
from typing import Optional

from sqlmodel import Field, Relationship
from core.models import BaseTable, SlugMixin


class Navigation(BaseTable, SlugMixin, table=True):
    title: str  # e.g. "main", "footer", "sidebar"
    is_active: bool = True  # Is this navigation active?

    items: list["NavigationItem"] = Relationship(back_populates="navigation")


class NavigationItem(BaseTable, SlugMixin, table=True):
    title: str
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
    # Define remote side for SQLAlchemy to disambiguate
    parent: Optional["NavigationItem"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "NavigationItem.id"},
    )
    children: list["NavigationItem"] = Relationship(back_populates="parent")
