# apps/cms/services/navigation.py
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.models.navigation import Navigation, NavigationItem
from apps.cms.schemas.navigation import (
    NavigationCreate,
    NavigationUpdate,
    NavigationItemCreate,
    NavigationItemUpdate,
)
from utils.text import slugify


# ---------------------------
# Navigation Services
# ---------------------------


async def create_navigation(
    data: NavigationCreate, session: AsyncSession
) -> Navigation:
    slug = data.slug or slugify(data.name)
    nav = Navigation(**data.model_dump(exclude={"slug"}), slug=slug)
    session.add(nav)
    try:
        await session.commit()
        await session.refresh(nav)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Navigation with this title/slug already exists",
        )

    # Explicitly load the items after refresh
    stmt = (
        select(Navigation)
        .where(Navigation.id == nav.id)
        .options(selectinload(Navigation.items))
    )
    result = await session.exec(stmt)
    return result.one()


async def get_navigation_by_id(nav_id: str, session: AsyncSession) -> Navigation | None:
    stmt = (
        select(Navigation)
        .where(Navigation.id == nav_id)
        .options(selectinload("Navigation.items"))
    )
    result = await session.exec(stmt)
    return result.one_or_none()


async def get_navigation_by_slug(slug: str, session: AsyncSession) -> Navigation | None:
    stmt = select(Navigation).where(Navigation.slug == slug)
    result = await session.exec(stmt)
    return result.one_or_none()


async def list_navigations(session: AsyncSession) -> list[Navigation]:
    stmt = select(Navigation).options(selectinload(Navigation.items))
    result = await session.exec(stmt)
    return result.all()


async def update_navigation(
    nav_id: str, data: NavigationUpdate, session: AsyncSession
) -> Navigation | None:
    nav = await get_navigation_by_id(nav_id, session)
    if not nav:
        return None

    for key, value in data.model_dump(exclude_unset=True, exclude={"slug"}).items():
        setattr(nav, key, value)

    if data.slug and data.slug != nav.slug:
        nav.slug = data.slug

    await session.commit()
    await session.refresh(nav)
    return nav


async def delete_navigation(nav_id: str, session: AsyncSession) -> bool:
    nav = await get_navigation_by_id(nav_id, session)
    if not nav:
        return False
    await session.delete(nav)
    await session.commit()
    return True


# ---------------------------
# NavigationItem Services
# ---------------------------


async def create_navigation_item(
    navigation_id: str, data: NavigationItemCreate, session: AsyncSession
) -> NavigationItem:
    slug = data.slug or slugify(data.title)
    item = NavigationItem(
        **data.model_dump(exclude={"slug"}), slug=slug, navigation_id=navigation_id
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def get_navigation_item_by_id(
    item_id: str, session: AsyncSession
) -> NavigationItem | None:
    return await session.get(NavigationItem, item_id)


async def list_navigation_items(
    navigation_id: str, session: AsyncSession
) -> list[NavigationItem]:
    stmt = (
        select(NavigationItem)
        .where(NavigationItem.navigation_id == navigation_id)
        .order_by(NavigationItem.order)
    )
    result = await session.exec(stmt)
    return result.all()


async def update_navigation_item(
    item_id: str, data: NavigationItemUpdate, session: AsyncSession
) -> NavigationItem | None:
    item = await get_navigation_item_by_id(item_id, session)
    if not item:
        return None

    for key, value in data.model_dump(exclude_unset=True, exclude={"slug"}).items():
        setattr(item, key, value)

    if data.slug and data.slug != item.slug:
        item.slug = data.slug

    await session.commit()
    await session.refresh(item)
    return item


async def delete_navigation_item(item_id: str, session: AsyncSession) -> bool:
    item = await get_navigation_item_by_id(item_id, session)
    if not item:
        return False
    await session.delete(item)
    await session.commit()
    return True
