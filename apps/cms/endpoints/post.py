# apps/cms/endpoints/post.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.cms.schemas.post import PostCreate, PostUpdate, PostRead
from apps.cms.services.post import PostService
from core.database import get_session

router = APIRouter()


def get_post_service(session: AsyncSession = Depends(get_session)) -> PostService:
    return PostService(session=session)


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Post",
)
async def create_post(
    data: PostCreate,
    service: PostService = Depends(get_post_service),
):
    return await service.create(data)


@router.get("/", response_model=list[PostRead], summary="List all Posts")
async def list_posts(service: PostService = Depends(get_post_service)):
    return await service.get_all()


@router.get("/{post_id}", response_model=PostRead, summary="Get a Post by ID")
async def get_post_by_id(
    post_id: str,
    service: PostService = Depends(get_post_service),
):
    post = await service.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.get("/slug/{slug}", response_model=PostRead, summary="Get a Post by Slug")
async def get_post_by_slug(
    slug: str,
    service: PostService = Depends(get_post_service),
):
    posts = await service.filter_by(slug=slug)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return posts[0]


@router.patch("/{post_id}", response_model=PostRead, summary="Update a Post")
async def update_post(
    post_id: str,
    data: PostUpdate,
    service: PostService = Depends(get_post_service),
):
    try:
        return await service.update_by_id(post_id, data.model_dump(exclude_unset=True))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )


@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Post"
)
async def delete_post(
    post_id: str,
    service: PostService = Depends(get_post_service),
):
    try:
        await service.delete_by_id(post_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return None
