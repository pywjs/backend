# core/schemas.py
from pydantic import BaseModel, ConfigDict
from ulid import ULID


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
    """Base schema for response data."""

    model_config = ConfigDict(from_attributes=True)
