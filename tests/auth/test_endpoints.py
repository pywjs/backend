# tests/auth/test_endpoints.py

import pytest
from httpx import AsyncClient


# ---------------------------------------------
# Test auth/token endpoint
# ---------------------------------------------
class TestToken:
    # Test login with valid credentials
    @pytest.mark.anyio
    async def test_token_success(self, client: AsyncClient, create_test_user):
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
    @pytest.mark.anyio
    async def test_token_wrong_password(self, client: AsyncClient, create_test_user):
        data = {
            "username": create_test_user.email,
            "password": "wrong password",
        }
        response = await client.post("/auth/token", data=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    # Test login with non-existing user
    @pytest.mark.anyio
    async def test_token_non_existing_user(self, client: AsyncClient):
        data = {
            "username": "no@example.com",
            "password": "test123",
        }
        response = await client.post("/auth/token", data=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    # Test login with inactive user
    @pytest.mark.anyio
    async def test_token_inactive_user(self, client: AsyncClient, create_inactive_user):
        data = {
            "username": create_inactive_user.email,
            "password": "test123",
        }
        response = await client.post("/auth/token", data=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Account is not active"

    # Test login with deleted user
    @pytest.mark.anyio
    async def test_token_deleted_user(self, client: AsyncClient, create_deleted_user):
        data = {
            "username": create_deleted_user.email,
            "password": "test123",
        }
        response = await client.post("/auth/token", data=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


# ---------------------------------------------
# Test auth/login endpoint
# ---------------------------------------------
class TestLogin:
    # Test login with valid credentials
    @pytest.mark.anyio
    async def test_login_success(self, client: AsyncClient, create_test_user):
        data = {
            "email": create_test_user.email,
            "password": "test123",
        }
        response = await client.post("/auth/login", json=data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    # Test login with the wrong password
    @pytest.mark.anyio
    async def test_login_wrong_password(self, client: AsyncClient, create_test_user):
        data = {
            "email": create_test_user.email,
            "password": "wrong password",
        }
        response = await client.post("/auth/login", json=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    # Test login with non-existing user
    @pytest.mark.anyio
    async def test_login_non_existing_user(self, client: AsyncClient):
        data = {
            "email": "no@example.com",
            "password": "test123",
        }
        response = await client.post("/auth/login", json=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    # Test login with inactive user
    @pytest.mark.anyio
    async def test_login_inactive_user(self, client: AsyncClient, create_inactive_user):
        data = {
            "email": create_inactive_user.email,
            "password": "test123",
        }
        response = await client.post("/auth/login", json=data)
        assert response.status_code == 403
        assert response.json()["detail"] == "Account is not active"

    # Test login with deleted user
    @pytest.mark.anyio
    async def test_login_deleted_user(self, client: AsyncClient, create_deleted_user):
        data = {
            "email": create_deleted_user.email,
            "password": "test123",
        }
        response = await client.post("/auth/login", json=data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


# ---------------------------------------------
# Test auth/refresh endpoint
# ---------------------------------------------
class TestRefresh:
    # Test refresh with valid refresh token
    @pytest.mark.anyio
    async def test_refresh_success(
        self, client: AsyncClient, create_test_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_test_user)
        form_data = {
            "grant_type": "refresh_token",
            "refresh_token": token_pair.refresh_token,
        }
        response = await client.post("/auth/refresh", data=form_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    # Test refresh with invalid refresh token *using access token*
    @pytest.mark.anyio
    async def test_refresh_invalid_token(
        self, client: AsyncClient, create_test_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_test_user)
        form_data = {
            "grant_type": "refresh_token",
            "refresh_token": token_pair.access_token,  # Use access token instead of refresh token
        }
        response = await client.post("/auth/refresh", data=form_data)
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]
