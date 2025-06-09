# apps/cms/services/post.py

from apps.cms.models.post import Post
from core.services import BaseService
from sqlmodel.ext.asyncio.session import AsyncSession


class PostService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)
