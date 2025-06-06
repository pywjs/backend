"""sg

Revision ID: 95f7cde3f6e1
Revises: 91e598afa5f7
Create Date: 2025-05-16 14:33:10.699936

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95f7cde3f6e1"
down_revision: Union[str, None] = "91e598afa5f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "page",
        "meta_keywords",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="meta_keywords::json",
    )
    op.alter_column(
        "page",
        "structured_data",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="structured_data::json",
    )
    op.alter_column(
        "page",
        "body_json",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="body_json::json",
    )
    op.alter_column(
        "post",
        "meta_keywords",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="meta_keywords::json",
    )
    op.alter_column(
        "post",
        "structured_data",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="structured_data::json",
    )
    op.alter_column(
        "post",
        "body_json",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="body_json::json",
    )
    op.alter_column(
        "post",
        "tags",
        existing_type=sa.VARCHAR(),
        type_=sa.JSON(),
        existing_nullable=True,
        postgresql_using="tags::json",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "post",
        "tags",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "post",
        "body_json",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "post",
        "structured_data",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "post",
        "meta_keywords",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "page",
        "body_json",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "page",
        "structured_data",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    op.alter_column(
        "page",
        "meta_keywords",
        existing_type=sa.JSON(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
