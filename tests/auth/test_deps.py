# tests/auth/test_deps.py
import pytest
from apps.auth.schemas import TokenPayload
from ulid import ULID
from apps.auth.deps import active_token, staff_token, admin_token, get_token_payload
from fastapi import HTTPException

# Get new ULID for test
TEMP_ULID = ULID()


# --------------------------------------------
# Fixtures
# --------------------------------------------
@pytest.fixture
def active_user():
    return TokenPayload(
        sub=TEMP_ULID,  # ULID format
        iat=1680000000,
        exp=1680003600,
        user_email="user@example.com",  # type: ignore
        is_active=True,
        is_staff=False,
        is_admin=False,
    )


@pytest.fixture
def staff_user(active_user):
    return active_user.model_copy(update={"is_staff": True, "is_admin": False})


@pytest.fixture
def admin_user(staff_user):
    return staff_user.model_copy(update={"is_admin": True})


# --------------------------------------------
# Token Payload Tests
# --------------------------------------------
@pytest.mark.anyio
async def test_token_payload(monkeypatch):
    class MockJWT:
        def decode_token(self, token: str, kind: str):
            return {
                "sub": TEMP_ULID,
                "iat": 1680000000,
                "exp": 1680003600,
                "user_email": "user@example.com",
                "is_active": True,
                "is_staff": False,
                "is_admin": False,
            }

    monkeypatch.setattr("apps.auth.deps.get_jwt", lambda: MockJWT())
    # test valid token
    result = await get_token_payload(token="valid-token")
    assert isinstance(result, TokenPayload)
    assert result.is_active is True

    # Test invalid token
    class MockJWTInvalid:
        def decode_token(self, token: str, kind: str):
            raise ValueError("Invalid token")

    monkeypatch.setattr("apps.auth.deps.get_jwt", lambda: MockJWTInvalid())
    with pytest.raises(HTTPException) as exc:
        await get_token_payload(token="invalid-token")

    assert exc.value.status_code == 401
    assert "Invalid token" in exc.value.detail


# --------------------------------------------
# Active Token Tests
# --------------------------------------------


@pytest.mark.anyio
async def test_active_token(active_user):
    # Test active token with valid active user
    active_user_payload = await active_token(active_user)
    assert active_user_payload == active_user

    # Test active token with invalid user
    inactive_user = active_user.model_copy(update={"is_active": False})
    with pytest.raises(HTTPException) as exc:
        await active_token(inactive_user)
    assert exc.value.status_code == 401
    assert "Inactive user" in exc.value.detail


# -----------------------------------------------
# Staff Token Tests
# -----------------------------------------------
@pytest.mark.anyio
async def test_staff_token(staff_user):
    # Test staff token with valid staff user
    staff_user_payload = await staff_token(staff_user)
    assert staff_user_payload == staff_user

    # Test staff token with invalid user
    non_staff_user = staff_user.model_copy(update={"is_staff": False})
    with pytest.raises(HTTPException) as exc:
        await staff_token(non_staff_user)
    assert exc.value.status_code == 403
    assert "Staff privileges required" in exc.value.detail


# -----------------------------------------------
# Admin Token Tests
# -----------------------------------------------
@pytest.mark.anyio
async def test_admin_token(admin_user):
    # Test admin token with valid admin user
    admin_user_payload = await admin_token(admin_user)
    assert admin_user_payload == admin_user

    # Test admin token with invalid user
    non_admin_user = admin_user.model_copy(update={"is_admin": False})
    with pytest.raises(HTTPException) as exc:
        await admin_token(non_admin_user)
    assert exc.value.status_code == 403
    assert "Admin privileges required" in exc.value.detail

    # Test staff is not admin
    staff_user = admin_user.model_copy(update={"is_admin": False})
    with pytest.raises(HTTPException) as exc:
        await admin_token(staff_user)
    assert exc.value.status_code == 403
    assert "Admin privileges required" in exc.value.detail
