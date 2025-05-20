# apps/auth/exceptions.py
from core.exceptions import BaseAppException


class BaseAuthException(Exception):
    """Base Exception for all authentication errors."""

    pass


class InvalidCredentialsException(BaseAuthException):
    """Exception raised for invalid credentials."""

    pass


class UserNotFoundException(BaseAuthException):
    """Exception raised when a user is not found in the database."""

    pass


class UserNotActiveException(BaseAppException):
    """Exception raised when a user is not active."""

    pass


class UserNotVerifiedException(BaseAppException):
    """Exception raised when a user is not verified."""

    pass


class UserAlreadyExistsException(BaseAppException):
    """Exception raised when a user already exists."""

    pass


class UserIsDeletedException(BaseAppException):
    """Exception raised when a user is deleted."""

    pass


class InvalidRefreshTokenException(BaseAuthException):
    """Exception raised when refresh token is invalid."""

    pass
