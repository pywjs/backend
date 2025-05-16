# apps/cms/endpoints/post.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.schemas.post import PostCreate, PostUpdate, PostRead
from apps.cms.services.post import (
    create_post,
    update_post,
    delete_post,
    get_post_by_id,
    get_post_by_slug,
    list_posts,
)

from core.database import get_session

router = APIRouter()


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Post",
)
async def create(data: PostCreate, session: AsyncSession = Depends(get_session)):
    return await create_post(data=data, session=session)


@router.get("/", response_model=list[PostRead], summary="List all Posts")
async def list_all(session: AsyncSession = Depends(get_session)):
    return await list_posts(session=session)


@router.get("/{post_id}", response_model=PostRead, summary="Get a Post by ID")
async def get_by_id(post_id: str, session: AsyncSession = Depends(get_session)):
    post = await get_post_by_id(post_id=post_id, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.get("/slug/{slug}", response_model=PostRead, summary="Get a Post by Slug")
async def get_by_slug(slug: str, session: AsyncSession = Depends(get_session)):
    post = await get_post_by_slug(slug=slug, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.patch("/{post_id}", response_model=PostRead, summary="Update a Post")
async def update(
    post_id: str, data: PostUpdate, session: AsyncSession = Depends(get_session)
):
    post = await update_post(post_id=post_id, data=data, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Post"
)
async def delete(post_id: str, session: AsyncSession = Depends(get_session)):
    post = await delete_post(post_id=post_id, session=session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return None
