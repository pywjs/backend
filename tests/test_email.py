# tests/test_email.py
from core.config import validate_smtp_from


def test_validate_smtp_from():
    assert (
        validate_smtp_from("Admin <admin@example.com>") == "Admin <admin@example.com>"
    )
    try:
        validate_smtp_from("invalid")
    except ValueError as e:
        assert "Invalid SMTP_FROM format" in str(e)
    try:
        validate_smtp_from("Admin <sdadsad@example.com")
    except ValueError as e:
        assert "Invalid SMTP_FROM format" in str(e)
