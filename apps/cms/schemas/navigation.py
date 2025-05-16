# apps/cms/schemas/navigation.py

from sqlmodel import SQLModel, Field
from ulid import ULID


class NavigationItemBase(SQLModel):
    title: str
    slug: str
    order: int = 0
    is_visible: bool = True
    is_external: bool = False
    page_id: str | None = None
    external_url: str | None = None
    parent_id: str | None = None


class NavigationItemCreate(NavigationItemBase):
    pass


class NavigationItemUpdate(SQLModel):
    title: str | None = None
    slug: str | None = None
    order: int | None = None
    is_visible: bool | None = None
    is_external: bool | None = None
    page_id: str | None = None
    external_url: str | None = None
    parent_id: str | None = None


class NavigationItemRead(NavigationItemBase):
    id: str | ULID | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    children: list["NavigationItemRead"] = []


class NavigationBase(SQLModel):
    name: str
    slug: str
    is_active: bool = True


class NavigationCreate(NavigationBase):
    pass


class NavigationUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None
    is_active: bool | None = None


class NavigationRead(NavigationBase):
    id: str | ULID | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    items: list[NavigationItemRead] = []


# Since the navigation items are self-referential, we need to use a forward reference
NavigationItemRead.model_rebuild()
