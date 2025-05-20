# tests/auth/test_endpoints.py
import pytest
from httpx import AsyncClient
from tests.conftest import save_user_to_db


# ---------------------------------------------
# Test auth/token endpoint
# ---------------------------------------------
@pytest.mark.anyio
async def test_login_token(client: AsyncClient, create_test_user):
    # Test login with valid credentials
    data = {
        "username": create_test_user.email,
        "password": "test123",
    }
    response = await client.post("/auth/token", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test login with the wrong password
    data["password"] = "wrong password"
    response = await client.post("/auth/token", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Test login with non-existing user
    data["username"] = "no-such-user@example.com"
    response = await client.post("/auth/token", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Test login with inactive user
    create_test_user.is_active = False
    await save_user_to_db(create_test_user)

    data["username"] = create_test_user.email
    data["password"] = "test123"
    response = await client.post("/auth/token", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Account is not active"
    # reset user to active
    create_test_user.is_active = True

    # Test login with deleted user
    create_test_user.is_deleted = True
    await save_user_to_db(create_test_user)
    data["username"] = create_test_user.email
    data["password"] = "test123"
    response = await client.post("/auth/token", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
