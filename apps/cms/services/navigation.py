# apps/cms/services/navigation.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import cast
from sqlalchemy.orm.attributes import InstrumentedAttribute
from apps.cms.models.navigation import Navigation, NavigationItem
from apps.cms.schemas.navigation import (
    NavigationCreateSchema,
    NavigationItemCreateSchema,
)
from core.services import BaseService, ResourceNotFoundException
from utils.text import slugify
from apps.cms.exceptions import InstanceAlreadyExists
from sqlalchemy.sql import Select
from collections.abc import Sequence


# ---------------------------
# Navigation Services
# ---------------------------
class NavigationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Navigation, session)
        self.session: AsyncSession = session

    async def create_navigation(self, data: NavigationCreateSchema) -> Navigation:
        slug = data.slug or slugify(data.title)
        instance = Navigation(**data.model_dump(exclude={"slug"}), slug=slug)
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except IntegrityError:
            await self.session.rollback()
            raise InstanceAlreadyExists

        # Explicitly load the items after refresh
        stmt: Select = (
            select(Navigation)
            .where(Navigation.id == instance.id)
            .options(selectinload(cast(InstrumentedAttribute, Navigation.items)))
        )
        result = await self.session.exec(stmt)
        return result.one()

    async def get_navigation_by_id(self, navigation_id: str) -> Navigation | None:
        stmt: Select = (
            select(Navigation)
            .where(Navigation.id == navigation_id)
            .options(selectinload(cast(InstrumentedAttribute, Navigation.items)))
        )
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def get_navigation_by_slug(self, slug: str) -> Navigation | None:
        stmt: Select = select(Navigation).where(Navigation.slug == slug)
        result = await self.session.exec(stmt)
        return result.one_or_none()


# ---------------------------
# NavigationItem Services
# ---------------------------
class NavigationItemService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(NavigationItem, session)
        self.session: AsyncSession = session

    async def create_navigation_item(
        self, navigation_id: str, data: NavigationItemCreateSchema
    ) -> NavigationItem:
        slug = data.slug or slugify(data.title)
        instance = NavigationItem(
            **data.model_dump(exclude={"slug"}),
            slug=slug,
            navigation_id=navigation_id,
        )
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
        except IntegrityError:
            await self.session.rollback()
            raise InstanceAlreadyExists

        # Explicitly load the navigation items after refresh
        stmt: Select = (
            select(NavigationItem)
            .where(NavigationItem.id == instance.id)
            .options(selectinload(cast(InstrumentedAttribute, NavigationItem.children)))
        )
        result = await self.session.exec(stmt)
        return result.one()

    async def get_navigation_item_by_id(
        self, navigation_item_id: str
    ) -> NavigationItem | None:
        stmt: Select = (
            select(NavigationItem)
            .where(NavigationItem.id == navigation_item_id)
            .options(selectinload(cast(InstrumentedAttribute, NavigationItem.children)))
        )
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def get_navigation_item_by_slug(self, slug: str) -> NavigationItem | None:
        stmt: Select = select(NavigationItem).where(NavigationItem.slug == slug)
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def list_navigation_items_by_navigation_id(
        self, navigation_id: str
    ) -> Sequence[
        NavigationItem
    ]:  # Sequence is a more general type than list, that can include list tuples, etc.
        stmt: Select = (
            select(NavigationItem)
            .where(NavigationItem.navigation_id == navigation_id)
            .options(selectinload(cast(InstrumentedAttribute, NavigationItem.children)))
        )
        result = await self.session.exec(stmt)
        return result.all()

    async def update_item(self, item_id: str, data: dict) -> NavigationItem | None:
        """Update a navigation item by ID."""
        try:
            # If a slug is provided but empty, generate from title if title exists
            if "slug" in data and not data["slug"] and "title" in data:
                data["slug"] = slugify(data["title"])

            return await self.update_by_id(item_id, data)
        except ResourceNotFoundException:
            return None
