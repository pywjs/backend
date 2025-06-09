# apps/cms/services/page.py

from sqlmodel.ext.asyncio.session import AsyncSession
from core.services import BaseService

from apps.cms.models.page import Page


class PageService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Page, session=session)
