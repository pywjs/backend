# core/models.py
from sqlmodel import Field, SQLModel, DateTime
from datetime import datetime
from ulid import ULID
from utils.time import current_time
from pydantic import ConfigDict


# Note: this class was named `BaseModel` in the previous code (versions before 0.1.1), but it was renamed to `_BaseModel` to avoid
# confusion with the `BaseModel` from Pydantic. Also, the _ states that this is a private class and should not be used directly.
class _BaseModel(SQLModel):
    """Base for non-table models and shared configuration."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow arbitrary types like ULID
        use_enum_values=True,  # Use enum values instead of enum instances
        json_encoders={
            ULID: lambda v: str(v),
        },  # Encode ULID as string
    )


class ULIDPrimaryKeyMixin:
    """Mixin for models with ULID primary keys."""

    # Stores ULID as a string (CHAR(26)) in the database
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)


"""
Note: without `type: ignore` PyCharm will complain about the type of `created_at` and `updated_at` fields:
`Expected type 'type | PydanticUndefinedType', got 'DateTime' instead`
"""


class TimestampMixin:
    """Mixin for models with created_at and updated_at timestamps."""

    created_at: datetime = Field(
        default_factory=current_time,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=current_time,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class PublishableMixin:
    """Mixin for models with publishable fields."""

    is_published: bool = Field(default=False)
    published_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))  # type: ignore
    unpublished_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class SlugMixin:
    """Mixin for models with slug fields."""

    slug: str = Field(index=True, unique=True)  # Unique slug for the model


class SoftDeleteMixin:
    """Mixin for models with soft delete fields."""

    is_deleted: bool = Field(default=False, index=True)  # Soft delete flag
    deleted_at: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))  # type: ignore


class BaseTable(
    _BaseModel, ULIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, table=False
):
    """Base class for all table models in the application."""

    # This class is not a table itself, but can be used as a base for other models
    # that need to inherit from it.
    pass
