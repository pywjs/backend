# apps/auth/exceptions.py


class BaseAuthException(Exception):
    """Base Exception for all authentication errors."""

    pass


class InvalidCredentialsException(BaseAuthException):
    """Exception raised for invalid credentials."""

    pass


class UserNotFoundException(BaseAuthException):
    """Exception raised when a user is not found in the database."""

    pass


class UserNotActiveException(BaseAuthException):
    """Exception raised when a user is not active."""

    pass


class UserNotVerifiedException(BaseAuthException):
    """Exception raised when a user is not verified."""

    pass


class UserAlreadyExistsException(BaseAuthException):
    """Exception raised when a user already exists."""

    pass


class UserIsDeletedException(BaseAuthException):
    """Exception raised when a user is deleted."""

    pass


class InvalidRefreshTokenException(BaseAuthException):
    """Exception raised when refresh token is invalid."""

    pass
