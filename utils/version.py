# utils/version.py

import tomllib
from functools import lru_cache

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def get_version():
    with open(BASE_DIR / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
        version = config["project"]["version"]
        if not version:
            version = "0.0.0"
        return config["project"]["version"]
