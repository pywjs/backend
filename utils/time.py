# utils/time.py
from datetime import datetime, UTC


def current_time():
    return datetime.now(UTC)
