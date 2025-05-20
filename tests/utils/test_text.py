# tests/utils/test_text.py

from utils.text import slugify


def test_slugify():
    # Basic test
    assert slugify("Hello World") == "hello-world"
    assert slugify("  Hello     World!  ") == "hello-world"
    assert slugify("FastAPI + SQLModel!") == "fastapi-sqlmodel"
    assert slugify("1234 Fast 🚀 CMS") == "1234-fast-cms"

    # Unicode normalization
    assert slugify("naïve café") == "naive-cafe"
    assert slugify("İstanbul!") == "istanbul"
    assert slugify("ümlaut ünicode") == "umlaut-unicode"

    # Special characters
    assert slugify("A--B__C") == "a-b__c"
    assert slugify("hello-world-again") == "hello-world-again"
    assert slugify("   -hello - world -  ") == "hello-world"
