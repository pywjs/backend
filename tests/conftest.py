# tests/conftest.py

import pytest
from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Synchronous test client."""
    with TestClient(app) as client:
        yield client
