# apps/users/models.py

from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from ulid import ULID


class User(SQLModel, table=True):
    id: str | ULID | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    email: EmailStr | None = Field(nullable=False, unique=True)
    hashed_password: str | None = Field(nullable=False)
    is_active: bool | None = Field(nullable=False)
    is_verified: bool | None = Field(nullable=False)
    is_staff: bool | None = Field(nullable=False)
    is_admin: bool | None = Field(nullable=False)
