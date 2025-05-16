# apps/cms/models/post.py
from .base import BasePost


class Post(BasePost, table=True):
    category: str | None = None
    tags: str | None = None

    @property
    def tag_list(self) -> list[str]:
        """Return a list of tags."""
        if self.tags:
            return self.tags.split(",")
        return []
