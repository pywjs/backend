# apps/auth/exceptions.py
from core.exceptions import BaseAppException
from enum import Enum, auto


class AuthErrorCode(Enum):
    INVALID_CREDENTIALS = auto
    USER_NOT_FOUND = auto
    USER_NOT_ACTIVE = auto
    USER_ALREADY_ACTIVE = auto


class AuthHTTPException(BaseAppException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code
