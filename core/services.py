# core/services.py

from enum import StrEnum
from typing import TypeVar, Type, Generic, Any
from sqlalchemy.sql import Select
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from core.exceptions import BaseServiceException
from utils.time import current_time

T = TypeVar("T", bound=SQLModel)


class DeleteMode(StrEnum):
    SOFT = "soft"
    HARD = "hard"


class ResourceNotFoundException(BaseServiceException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} with identifier '{identifier}' not found.")


class SoftDeleteNotSupportedException(BaseServiceException):
    """Exception raised when soft delete is not supported for a model."""

    def __init__(self, model: Type[SQLModel]):
        super().__init__(f"Soft delete is not supported for model '{model.__name__}'.")


class BaseService(Generic[T]):
    def __init__(
        self,
        model: Type[T],
        session: AsyncSession,
        delete_mode: DeleteMode = DeleteMode.SOFT,
    ):
        self.session = session
        self.model = model
        self.delete_mode = delete_mode

    async def get_by_id(self, id_: str) -> T | None:
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def filter_by(self, **kwargs) -> list[T]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.exec(stmt)
        return result.all()

    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        result = await self.session.exec(stmt)
        return result.all()

    async def count(self, stmt: Select | None = None) -> int:
        stmt = stmt or select(func.count()).select_from(self.model)
        result = await self.session.exec(stmt)
        return result.one()

    async def paginate(
        self,
        stmt: Select | None = None,
        page: int = 1,
        page_size: int = 20,
        order_by: list | None = None,
    ) -> list[T]:
        offset = (page - 1) * page_size
        stmt = (stmt or select(self.model)).offset(offset).limit(page_size)
        if order_by:
            stmt = stmt.order_by(*order_by)
        result = await self.session.exec(stmt)
        return result.all()

    async def paginate_with_total(
        self,
        stmt: Select | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[int, list[T]]:
        count_stmt = (
            select(func.count()).select_from(self.model)
            if stmt is None
            else select(func.count()).select_from(stmt.subquery())
        )
        total = await self.count(count_stmt)
        items = await self.paginate(stmt, page=page, page_size=page_size)
        return total, items

    async def create(self, data: dict[str, Any] | SQLModel) -> T:
        """Create a new model instance. Override for custom logic."""
        if isinstance(data, dict):
            instance = self.model(**data)
        else:
            instance = data
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: T, data: dict[str, Any]) -> T:
        """Update fields on an existing instance. (PARTIAL UPDATE)"""
        for key, value in data.items():
            setattr(instance, key, value)
        # update the updated_at field if it exists
        if hasattr(instance, "updated_at"):
            instance.updated_at = current_time()
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update_by_id(self, id_: str, data: dict[str, Any]) -> T:
        """Update a model instance by ID."""
        instance = await self.get_by_id(id_)
        if not instance:
            raise ResourceNotFoundException(self.model.__name__, id_)
        return await self.update(instance, data)

    async def delete(self, instance: T) -> None:
        """Delete a model instance by respective delete mode."""
        if self.delete_mode == DeleteMode.SOFT:
            if not hasattr(instance, "is_deleted"):
                raise SoftDeleteNotSupportedException(self.model)
            instance.is_deleted = True
            self.session.add(instance)
        elif self.delete_mode == DeleteMode.HARD:
            await self.session.delete(instance)
        await self.session.commit()

    async def delete_by_id(self, id_: str) -> T:
        """Delete a model instance by ID."""
        instance = await self.get_by_id(id_)
        if not instance:
            raise ResourceNotFoundException(self.model.__name__, id_)
        await self.delete(instance)
        return instance

    def __repr__(self):
        return f"<{self.__class__.__name__} model={self.model.__name__}>"
