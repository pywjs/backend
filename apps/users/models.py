# apps/users/models.py

from sqlmodel import Field
from pydantic import EmailStr
from core.models import BaseTable


class User(BaseTable, table=True):
    email: EmailStr = Field(nullable=False, unique=True)
    hashed_password: str

    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_admin: bool = Field(default=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email
