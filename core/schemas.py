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


class Optionals(_BaseSchema):
    """
    Base for mixins with optional fields grouped for reuse across request/update schemas.
    Allows shared validation or metadata injection in the future.
    """

    pass


# -> Base for input/request schemas
class RequestSchema(_BaseSchema):
    """Base schema for request data."""

    pass


# <- Base for output/response schemas
class ResponseSchema(_BaseSchema):
    model_config = ConfigDict(from_attributes=True)


class ULIDPrimaryKeyRequest(RequestSchema):
    id: ULID


class ULIDPrimaryKeyResponse(ResponseSchema):
    id: str


class TimestampResponse(ResponseSchema):
    created_at: datetime
    updated_at: datetime


# Note: those fields should not be updated from the request.
# Instead, they should be set by the server when creating or updating the record.
class TimestampRequest(RequestSchema):
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class PublishableCreateRequest(RequestSchema):
    is_published: bool = False


class PublishableUpdateRequest(RequestSchema):
    is_published: bool | None = None


class PublishableResponse(ResponseSchema):
    is_published: bool | None = False
    published_at: datetime | None = None
    unpublished_at: datetime | None = None


class SlugRequest(RequestSchema):
    # This schema is here just for consistency.
    # In general case, we want to generate the slug from the title or other fields programmatically.
    slug: str | None = None


class SlugCreateRequest(RequestSchema):
    slug: str


class SlugUpdateRequest(RequestSchema):
    slug: str | None = None


class SlugResponse(ResponseSchema):
    slug: str
