# apps/cms/endpoints/navigation.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from apps.cms.services.navigation import NavigationService, NavigationItemService
from core.database import get_session
from apps.cms.schemas.navigation import (
    NavigationCreateSchema,
    NavigationUpdateSchema,
    NavigationResponseSchema,
    NavigationItemCreateSchema,
    NavigationItemUpdateSchema,
    NavigationItemResponseSchema,
)
from apps.cms.exceptions import InstanceAlreadyExists

router = APIRouter()


# ---------------------------
# Navigation Endpoints
# ---------------------------
@router.post(
    "/", response_model=NavigationResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create(
    data: NavigationCreateSchema, session: AsyncSession = Depends(get_session)
):
    service = NavigationService(session)
    try:
        return await service.create_navigation(data)
    except InstanceAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Navigation with this title/slug already exists"
        )


@router.get("/", response_model=list[NavigationResponseSchema])
async def list_all(session: AsyncSession = Depends(get_session)):
    service = NavigationService(session)
    return await service.get_all()


@router.get("/{navigation_id}", response_model=NavigationResponseSchema)
async def get_by_id(navigation_id: str, session: AsyncSession = Depends(get_session)):
    service = NavigationService(session)
    nav = await service.get_navigation_by_id(navigation_id)
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return nav


@router.patch("/{navigation_id}", response_model=NavigationResponseSchema)
async def update_navigation(
    navigation_id: str,
    data: NavigationUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    service = NavigationService(session)
    nav = await service.update_by_id(navigation_id, data.model_dump())
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return nav


@router.delete("/{navigation_id}", status_code=204)
async def delete_navigation(
    navigation_id: str, session: AsyncSession = Depends(get_session)
):
    service = NavigationService(session)
    nav = await service.delete_by_id(navigation_id)
    if not nav:
        raise HTTPException(status_code=404, detail="Navigation not found")
    return None


# ---------------------------
# Navigation Item Endpoints
# ---------------------------
@router.post(
    "/{navigation_id}/items",
    response_model=NavigationItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_navigation_item(
    navigation_id: str,
    data: NavigationItemCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    service = NavigationItemService(session)
    try:
        return await service.create_navigation_item(navigation_id, data)
    except InstanceAlreadyExists:
        raise HTTPException(
            status_code=400,
            detail="Navigation item with this title/slug already exists",
        )


@router.get("/{navigation_id}/items", response_model=list[NavigationItemResponseSchema])
async def list_items(navigation_id: str, session: AsyncSession = Depends(get_session)):
    service = NavigationItemService(session)
    return await service.get_items_by_navigation_id(navigation_id)


@router.get("/items/{item_id}", response_model=NavigationItemResponseSchema)
async def get_item(item_id: str, session: AsyncSession = Depends(get_session)):
    service = NavigationItemService(session)
    item = await service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return item


@router.patch("/items/{item_id}", response_model=NavigationItemResponseSchema)
async def update_item(
    item_id: str,
    data: NavigationItemUpdateSchema,
    session: AsyncSession = Depends(get_session),
):
    service = NavigationItemService(session)
    item = await service.update_item(item_id, data.model_dump())
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str, session: AsyncSession = Depends(get_session)):
    service = NavigationItemService(session)
    item = await service.delete_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Navigation item not found")
    return None
