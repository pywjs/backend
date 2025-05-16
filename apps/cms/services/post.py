# apps/cms/services/post.py

from apps.cms.schemas.post import PostCreate, PostUpdate
from apps.cms.models.post import Post
from utils.text import slugify
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_post(data: PostCreate, session: AsyncSession) -> Post:
    slug = data.slug or slugify(data.title)
    post = Post(**data.model_dump(exclude={"slug"}), slug=slug)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_post_by_id(post_id: str, session: AsyncSession) -> Post | None:
    return await session.get(Post, post_id)


async def get_post_by_slug(slug: str, session: AsyncSession) -> Post | None:
    stmt = select(Post).where(Post.slug == slug)
    result = await session.exec(stmt)
    return result.one_or_none()


async def list_posts(session: AsyncSession) -> list[Post]:
    stmt = select(Post)
    result = await session.exec(stmt)
    return result.all()


async def update_post(
    post_id: str, data: PostUpdate, session: AsyncSession
) -> Post | None:
    post = await get_post_by_id(post_id, session)
    if not post:
        return None

    # Check if is_published is being changed
    is_published_changed = "is_published" in data.model_dump(exclude_unset=True)
    was_published = post.is_published

    # Update post attributes
    for key, value in data.model_dump(exclude_unset=True, exclude={"slug"}).items():
        setattr(post, key, value)

    if data.slug and data.slug != post.slug:
        post.slug = data.slug

    # Handle publishing status changes
    if is_published_changed:
        if post.is_published and not was_published:
            post.publish()
        elif not post.is_published and was_published:
            post.unpublish()
    else:
        # Update timestamp if other fields were changed
        post.update_timestamp()

    await session.commit()
    await session.refresh(post)
    return post


async def delete_post(post_id: str, session: AsyncSession) -> bool:
    post = await get_post_by_id(post_id, session)
    if not post:
        return False

    await session.delete(post)
    await session.commit()
    return True
