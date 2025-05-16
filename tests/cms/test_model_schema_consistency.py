# tests/cms/test_model_schema_consistency.py

from sqlmodel import SQLModel
from typing import Type

from apps.cms.models.page import Page
from apps.cms.models.post import Post

from apps.cms.schemas.post import PostCreate
from apps.cms.schemas.page import PageCreate


def get_model_fields(model: Type[SQLModel]) -> set[str]:
    return {name for name, field in model.model_fields.items()}


def get_table_fields(model: Type[SQLModel]) -> set[str]:
    return {c.name for c in model.__table__.columns}


def get_schema_fields(schema: Type[SQLModel]) -> set[str]:
    return {name for name, field in schema.model_fields.items()}


def test_page_schema_matches_model():
    model_fields = get_model_fields(Page)
    schema_fields = get_schema_fields(PageCreate)

    # Optional: ignore common fields like timestamps
    excluded = {"id", "created_at", "updated_at", "published_at"}
    model_fields -= excluded
    schema_fields -= excluded

    assert schema_fields.issubset(model_fields), (
        f"Schema has fields not in model: {schema_fields - model_fields}"
    )
    assert model_fields.issubset(schema_fields | excluded), (
        f"Model has fields not in schema: {model_fields - schema_fields}"
    )


def test_post_schema_matches_model():
    model_fields = get_model_fields(Post)
    schema_fields = get_schema_fields(PostCreate)

    excluded = {"id", "created_at", "updated_at", "published_at"}
    model_fields -= excluded
    schema_fields -= excluded

    assert schema_fields.issubset(model_fields), (
        f"Schema has fields not in model: {schema_fields - model_fields}"
    )
    assert model_fields.issubset(schema_fields | excluded), (
        f"Model has fields not in schema: {model_fields - schema_fields}"
    )
