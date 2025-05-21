# apps/cms/schemas/navigation.py
from pydantic import field_serializer

from core.schemas import (
    RequestSchema,
    SlugCreateRequest,
    SlugUpdateRequest,
    SlugResponse,
    ResponseSchema,
    ULIDPrimaryKeyResponse,
    Optionals,
)


class NavigationItemOptionals(Optionals):
    is_visible: bool | None = None
    is_external: bool | None = None
    page_id: str | None = None
    external_url: str | None = None
    parent_id: str | None = None


class NavigationItemCreateSchema(
    NavigationItemOptionals,
    SlugCreateRequest,
    RequestSchema,
):
    title: str
    order: int = 0


class NavigationItemUpdateSchema(
    NavigationItemOptionals,
    SlugUpdateRequest,
    RequestSchema,
):
    title: str | None = None
    order: int | None = None


class NavigationItemResponseSchema(
    NavigationItemOptionals, ULIDPrimaryKeyResponse, SlugResponse, ResponseSchema
):
    title: str
    order: int
    children: list["NavigationItemResponseSchema"] = []

    @field_serializer("children", when_used="always")
    def default_children(self, value):
        return value or []


class NavigationOptionals(Optionals):
    pass


class NavigationCreateSchema(
    NavigationOptionals,
    SlugCreateRequest,
    RequestSchema,
):
    name: str
    is_active: bool = True


class NavigationUpdateSchema(
    NavigationOptionals,
    SlugUpdateRequest,
    RequestSchema,
):
    name: str | None = None
    is_active: bool | None = None


class NavigationResponseSchema(
    NavigationOptionals, ULIDPrimaryKeyResponse, SlugResponse, ResponseSchema
):
    name: str
    is_active: bool = True
    items: list[NavigationItemResponseSchema] = []


# Since the navigation items are self-referential, we need to use a forward reference
NavigationItemResponseSchema.model_rebuild()
