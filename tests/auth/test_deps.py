# tests/auth/test_deps.py

import pytest
from fastapi import FastAPI, Depends
from httpx import AsyncClient

from apps.auth.deps import active_user_token, staff_user_token, admin_user_token
from apps.users.models import User


@pytest.fixture
def app() -> FastAPI:
    """Override the default app fixture for this module with protected routes."""
    app = FastAPI()

    @app.get("/protected")
    async def protected_route(token_user: User = Depends(active_user_token)):
        return {"message": "Protected route", "user": token_user.email}

    @app.get("/staff")
    async def staff_route(token_user: User = Depends(staff_user_token)):
        return {"message": "Staff route", "user": token_user.email}

    @app.get("/admin")
    async def admin_route(token_user: User = Depends(admin_user_token)):
        return {"message": "Admin route", "user": token_user.email}

    return app


class TestDeps:
    # Test active user token success
    @pytest.mark.anyio
    async def test_active_user_token_success(
        self, client: AsyncClient, create_test_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_test_user)
        response = await client.get(
            "/protected", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 200

    # Test active user token failure with inactive user
    @pytest.mark.anyio
    async def test_active_user_token_failure_inactive(
        self, client: AsyncClient, create_inactive_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_inactive_user)
        response = await client.get(
            "/protected", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Inactive user"}

    # Test staff user token success
    @pytest.mark.anyio
    async def test_staff_user_token_success(
        self, client: AsyncClient, create_staff_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_staff_user)
        response = await client.get(
            "/staff", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 200

    # Test staff user token failure with non-staff user
    @pytest.mark.anyio
    async def test_staff_user_token_failure_non_staff(
        self, client: AsyncClient, create_test_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_test_user)
        response = await client.get(
            "/staff", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 403
        assert "Permission denied" in response.json()["detail"]

    # Test admin user token success
    @pytest.mark.anyio
    async def test_admin_user_token_success(
        self, client: AsyncClient, create_admin_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_admin_user)
        response = await client.get(
            "/admin", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 200

    # Test admin user token failure with non-admin user (normal user)
    @pytest.mark.anyio
    async def test_admin_user_token_failure_non_admin(
        self, client: AsyncClient, create_test_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_test_user)
        response = await client.get(
            "/admin", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 403
        assert "Permission denied" in response.json()["detail"]

    # Test admin user token failure with non-admin user (staff user)
    @pytest.mark.anyio
    async def test_admin_user_token_failure_staff(
        self, client: AsyncClient, create_staff_user, get_token_pair_for_user
    ):
        token_pair = await get_token_pair_for_user(create_staff_user)
        response = await client.get(
            "/admin", headers={"Authorization": f"Bearer {token_pair.access_token}"}
        )
        assert response.status_code == 403
        assert "Permission denied" in response.json()["detail"]
