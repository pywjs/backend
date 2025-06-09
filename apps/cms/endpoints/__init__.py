# apps/cms/endpoints/__init__.py

from fastapi import APIRouter
from .post import router as post_router
from .page import router as page_router
from .navigation import router as navigation_router

router = APIRouter()

router.include_router(page_router, prefix="/pages", tags=["cms/pages"])
router.include_router(post_router, prefix="/posts", tags=["cms/posts"])
router.include_router(
    navigation_router, prefix="/navigations", tags=["cms/navigations"]
)
