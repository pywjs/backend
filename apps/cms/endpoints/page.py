# apps/cms/endpoints/page.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.schemas.page import PageCreate, PageUpdate, PageRead
from apps.cms.services.page import (
    create_page,
    update_page,
    delete_page,
    get_page_by_id,
    get_page_by_slug,
    list_pages,
)
from core.database import get_session

router = APIRouter()


@router.post("/", response_model=PageRead, status_code=status.HTTP_201_CREATED)
async def create(data: PageCreate, session: AsyncSession = Depends(get_session)):
    return await create_page(data=data, session=session)


@router.get("/", response_model=list[PageRead])
async def list_all(session: AsyncSession = Depends(get_session)):
    return await list_pages(session=session)


@router.get("/{page_id}", response_model=PageRead)
async def get_by_id(page_id: str, session: AsyncSession = Depends(get_session)):
    page = await get_page_by_id(page_id=page_id, session=session)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.get("/slug/{slug}", response_model=PageRead)
async def get_by_slug(slug: str, session: AsyncSession = Depends(get_session)):
    page = await get_page_by_slug(slug=slug, session=session)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.patch("/{page_id}", response_model=PageRead)
async def update(
    page_id: str, data: PageUpdate, session: AsyncSession = Depends(get_session)
):
    page = await update_page(page_id=page_id, data=data, session=session)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(page_id: str, session: AsyncSession = Depends(get_session)):
    page = await delete_page(page_id=page_id, session=session)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return None
