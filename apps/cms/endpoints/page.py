# apps/cms/endpoints/page.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.schemas.page import PageCreate, PageUpdate, PageRead
from apps.cms.services.page import PageService
from core.database import get_session

router = APIRouter()


def get_page_service(session: AsyncSession = Depends(get_session)) -> PageService:
    return PageService(session=session)


@router.post("/", response_model=PageRead, status_code=status.HTTP_201_CREATED)
async def create_page(
    data: PageCreate,
    service: PageService = Depends(get_page_service),
):
    return await service.create(data)


@router.get("/", response_model=list[PageRead])
async def list_pages(service: PageService = Depends(get_page_service)):
    return await service.get_all()


@router.get("/{page_id}", response_model=PageRead)
async def get_page_by_id(
    page_id: str,
    service: PageService = Depends(get_page_service),
):
    page = await service.get_by_id(page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.get("/slug/{slug}", response_model=PageRead)
async def get_page_by_slug(
    slug: str,
    service: PageService = Depends(get_page_service),
):
    pages = await service.filter_by(slug=slug)
    if not pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return pages[0]


@router.patch("/{page_id}", response_model=PageRead)
async def update_page(
    page_id: str,
    data: PageUpdate,
    service: PageService = Depends(get_page_service),
):
    try:
        return await service.update_by_id(page_id, data.model_dump(exclude_unset=True))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    page_id: str,
    service: PageService = Depends(get_page_service),
):
    try:
        await service.delete_by_id(page_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
