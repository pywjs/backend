# core/exceptions.py


class BaseSecurityException(Exception):
    """Base class for all token-related exceptions."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class BaseServiceException(Exception):
    """Base class for all exceptions."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
