# apps/cms/models/page.py
from sqlmodel import SQLModel
from .base import BasePage


class Page(SQLModel, BasePage, table=True):
    order_in_navigation: int = (
        -1
    )  # Order in navigation, if < 0, not shown in navigation
