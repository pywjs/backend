# apps/cms/endpoints/navigation.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.schemas.navigation import (
    NavigationCreate,
    NavigationUpdate,
    NavigationRead,
    NavigationItemCreate,
    NavigationItemUpdate,
    NavigationItemRead,
)
from apps.cms.services.navigation import (
    create_navigation,
    list_navigations,
    get_navigation_by_id,
    update_navigation,
    delete_navigation,
    create_navigation_item,
    list_navigation_items,
    get_navigation_item_by_id,
    update_navigation_item,
    delete_navigation_item,
)
from core.database import get_session

router = APIRouter()

# --- Navigation ---


@router.post("/", response_model=NavigationRead, status_code=status.HTTP_201_CREATED)
async def create(data: NavigationCreate, session: AsyncSession = Depends(get_session)):
    return await create_navigation(data=data, session=session)


@router.get("/", response_model=list[NavigationRead])
async def list_all(session: AsyncSession = Depends(get_session)):
    return await list_navigations(session=session)


@router.get("/{nav_id}", response_model=NavigationRead)
async def get_by_id(nav_id: str, session: AsyncSession = Depends(get_session)):
    nav = await get_navigation_by_id(nav_id=nav_id, session=session)
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return nav


@router.patch("/{nav_id}", response_model=NavigationRead)
async def update(
    nav_id: str, data: NavigationUpdate, session: AsyncSession = Depends(get_session)
):
    nav = await update_navigation(nav_id=nav_id, data=data, session=session)
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return nav


@router.delete("/{nav_id}", status_code=204)
async def delete(nav_id: str, session: AsyncSession = Depends(get_session)):
    nav = await delete_navigation(nav_id=nav_id, session=session)
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return None


# --- Navigation Items ---


@router.post(
    "/{nav_id}/items",
    response_model=NavigationItemRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_item(
    navigation_id: str,
    data: NavigationItemCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_navigation_item(
        navigation_id=navigation_id, data=data, session=session
    )


@router.get("/{nav_id}/items", response_model=list[NavigationItemRead])
async def list_items(navigation_id: str, session: AsyncSession = Depends(get_session)):
    return await list_navigation_items(navigation_id=navigation_id, session=session)


@router.get("/items/{item_id}", response_model=NavigationItemRead)
async def get_item(item_id: str, session: AsyncSession = Depends(get_session)):
    item = await get_navigation_item_by_id(item_id=item_id, session=session)
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return item


@router.patch("/items/{item_id}", response_model=NavigationItemRead)
async def update_item(
    item_id: str,
    data: NavigationItemUpdate,
    session: AsyncSession = Depends(get_session),
):
    item = await update_navigation_item(item_id=item_id, data=data, session=session)
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str, session: AsyncSession = Depends(get_session)):
    item = await delete_navigation_item(item_id=item_id, session=session)
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return None
