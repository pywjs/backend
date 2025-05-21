# core/schemas.py
from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID
from datetime import datetime


# Since the schemas are pure API schemas, not tied to the DB, we use BaseModel from Pydantic instead of the SQLModel.
class _BaseSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Allow arbitrary types like ULID
        use_enum_values=True,  # Use enum values instead of enum instances
        json_encoders={
            ULID: lambda v: str(v),
        },  # Encode ULID as string
    )


# -> Base for input/request schemas
class RequestSchema(_BaseSchema):
    """Base schema for request data."""

    pass


# <- Base for output/response schemas
class ResponseSchema(_BaseSchema):
    """Base schema for response data.
    Sets the `from_attributes` config to True, so that the model will be created from attributes
    """

    model_config = ConfigDict(from_attributes=True)


class ULIDPrimaryKeyRequest(RequestSchema):
    """Mixin for request schemas with ULID primary keys.
    Fields:
        - id: ULID primary key
    """

    id: ULID


class ULIDPrimaryKeyResponse(ResponseSchema):
    id: str


class TimestampResponse(ResponseSchema):
    created_at: datetime
    updated_at: datetime


class TimestampRequest(RequestSchema):
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class PublishableRequest(RequestSchema):
    is_published: bool | None = False
    published_at: datetime | None = None
    unpublished_at: datetime | None = None


class PublishableResponse(ResponseSchema):
    is_published: bool | None = False
    published_at: datetime | None = None
    unpublished_at: datetime | None = None
