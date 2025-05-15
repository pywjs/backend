# core/security/crypto.py

from passlib.context import CryptContext
from typing import Literal


class PasswordHasher:
    def __init__(self, scheme: Literal["bcrypt", "argon2"] = "argon2"):
        if scheme == "argon2":
            self.context = CryptContext(
                schemes=["argon2"],
                deprecated="auto",
                argon2__type="ID",
                argon2__memory_cost=65536,  # 64 MB
                argon2__time_cost=2,
                argon2__parallelism=4,
                argon2__hash_len=16,
                argon2__salt_size=16,
            )
        elif scheme == "bcrypt":
            self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        else:
            raise ValueError(f"Unsupported hashing scheme: {scheme}")

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)
