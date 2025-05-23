"""sg

Revision ID: fea99af9badf
Revises: fb5c873dd820
Create Date: 2025-05-20 09:55:47.685560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "fea99af9badf"
down_revision: Union[str, None] = "fb5c873dd820"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("upload", sa.Column("is_deleted", sa.Boolean(), nullable=False))
    op.add_column(
        "upload", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.alter_column(
        "upload",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "upload",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.create_index(
        op.f("ix_upload_is_deleted"), "upload", ["is_deleted"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_upload_is_deleted"), table_name="upload")
    op.alter_column(
        "upload",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        "upload",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.drop_column("upload", "deleted_at")
    op.drop_column("upload", "is_deleted")
    # ### end Alembic commands ###
