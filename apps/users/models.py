# apps/users/models.py

from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from ulid import ULID


class User(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(ULID()), primary_key=True)
    email: EmailStr | None = Field(nullable=False, unique=True)
    hashed_password: str
    is_active: bool | None = Field(default=True)
    is_verified: bool | None = Field(default=False)
    is_staff: bool | None = Field(default=False)
    is_admin: bool | None = Field(default=False)
