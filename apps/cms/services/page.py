# apps/cms/services/page.py

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.models.page import Page
from apps.cms.schemas.page import PageCreate, PageUpdate
from utils.text import slugify


async def create_page(data: PageCreate, session: AsyncSession) -> Page:
    slug = data.slug or slugify(data.title)
    page = Page(**data.model_dump(exclude={"slug"}), slug=slug)
    session.add(page)
    await session.commit()
    await session.refresh(page)
    return page


async def get_page_by_id(page_id: str, session: AsyncSession) -> Page | None:
    return await session.get(Page, page_id)


async def get_page_by_slug(slug: str, session: AsyncSession) -> Page | None:
    stmt = select(Page).where(Page.slug == slug)
    result = await session.exec(stmt)
    return result.one_or_none()


async def list_pages(session: AsyncSession) -> list[Page]:
    stmt = select(Page)
    result = await session.exec(stmt)
    return result.all()


async def update_page(
    page_id: str, data: PageUpdate, session: AsyncSession
) -> Page | None:
    page = await get_page_by_id(page_id, session)
    if not page:
        return None

    for key, value in data.model_dump(exclude_unset=True, exclude={"slug"}).items():
        setattr(page, key, value)

    if data.slug and data.slug != page.slug:
        page.slug = data.slug

    await session.commit()
    await session.refresh(page)
    return page


async def delete_page(page_id: str, session: AsyncSession) -> bool:
    page = await get_page_by_id(page_id, session)
    if not page:
        return False

    await session.delete(page)
    await session.commit()
    return True
