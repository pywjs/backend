# apps/uploads/storages/base.py

from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorage(ABC):
    name: str

    @abstractmethod
    async def upload_file(self, file: BinaryIO, file_name: str) -> str: ...

    @abstractmethod
    async def delete_file(self, file_name: str) -> None: ...

    @abstractmethod
    async def get_url(self, file_name: str) -> str: ...
