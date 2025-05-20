# core/exceptions.py


class BaseAppException(Exception):
    """Base class for all exceptions."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class BaseSecurityException(BaseAppException):
    """Base class for all token-related exceptions."""

    def __init__(self, message: str):
        super().__init__(message)


class BaseServiceException(BaseAppException):
    """Base class for all exceptions."""

    def __init__(self, message: str):
        super().__init__(message)
