# utils/text.py
import re
import unicodedata


def slugify(text: str) -> str:
    """Generate a clean, URL-safe slug from the given text."""
    text = str(text).lower()  # Convert to lowercase
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", " ", text).strip()  # Remove non-alphanumeric characters
    text = re.sub(r"[-\s]+", "-", text).strip(
        "-"
    )  # Replace spaces and hyphens with a single hyphen
    return text
