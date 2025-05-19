# core/exceptions.py


class BaseServiceException(Exception):
    """Base class for all exceptions."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
