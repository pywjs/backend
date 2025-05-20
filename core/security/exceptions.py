# core/security/exceptions.py
from core.exceptions import BaseSecurityException


class InvalidTokenException(BaseSecurityException):
    """Invalid token exception."""

    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)


class ExpiredTokenException(BaseSecurityException):
    """Expired token exception."""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)


class InvalidTokenTypeException(BaseSecurityException):
    """Invalid token type exception."""

    def __init__(self, message: str = "Invalid token type"):
        super().__init__(message)
