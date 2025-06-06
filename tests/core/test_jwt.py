# tests/core/test_jwt.py
import pytest
from core.security.jwt import JWT, TokenUser, TokenPair, JWTTokenPayload
from utils.time import current_time
from core.security.exceptions import ExpiredTokenException


@pytest.fixture
def jwt():
    return JWT(
        secret="secret",
    )


@pytest.fixture
def token_user():
    return TokenUser(
        id="01JVPDJAHW6SCX3T93X85EP4A2",
        email="user@example.com",
        is_verified=False,
        is_active=True,
        is_staff=False,
        is_admin=False,
    )


@pytest.fixture
def staff_token_user():
    return TokenUser(
        id="01JVPDJAHW6SCX3T93X85EP4A2",
        email="staff@example.com",
        is_verified=True,
        is_active=True,
        is_staff=True,
        is_admin=False,
    )


def test_token_pair(jwt, token_user):
    # Test that the token pair is created correctly
    token_pair = jwt.token_pair(token_user)
    assert isinstance(token_pair, TokenPair)
    assert token_pair.access_token is not None
    assert token_pair.refresh_token is not None

    # Test that the access token is valid
    assert jwt.verify(token_pair.access_token, token_type="access") is True

    # Test that access token contains the correct payload
    token_data = jwt.token_data(token_pair.access_token)
    assert token_data is not None
    assert token_data.sub == token_user.id
    assert token_data.email == token_user.email

    # Test that the refresh token is valid
    refresh_token = jwt.refresh_token(token_user)
    assert refresh_token is not None
    assert jwt.verify(refresh_token, token_type="refresh") is True


# Issue #6 Make sure that the refresh token is minimal
def test_refresh_token_is_minimal(jwt, token_user):
    token = jwt.refresh_token(token_user)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Manually decode to inspect the full payload
    payload = jwt._decode_jwt(token)

    assert payload.get("sub") == token_user.id
    assert payload.get("token_type") == "refresh"

    # Ensure only minimal fields are present
    allowed_keys = ["sub", "iat", "exp", "token_type", "id"]
    assert all(key in allowed_keys for key in payload.keys())


def test_invalid_token_type_rejected(jwt, token_user):
    # Test that the verify method rejects invalid token types
    access_token = jwt.access_token(token_user)
    # verify the access_token as refresh token [should fail]
    assert jwt.verify(access_token, token_type="refresh") is False


def test_expired_token_is_invalid(jwt, token_user):
    from datetime import timedelta

    past = current_time() - timedelta(days=1)
    payload = {
        "sub": token_user.id,
        "iat": past,
        "exp": past + timedelta(minutes=1),
        "token_type": "access",
    }
    token = jwt._encode_jwt(JWTTokenPayload.model_construct(**payload))
    with pytest.raises(ExpiredTokenException):
        jwt.verify(token, token_type="access")


def test_staff_is_not_admin(jwt, staff_token_user):
    token_pair = jwt.token_pair(staff_token_user)
    assert isinstance(token_pair, TokenPair)
    assert token_pair.access_token is not None
    assert token_pair.refresh_token is not None
    # Test that the access token is valid
    assert jwt.verify(token_pair.access_token, token_type="access") is True
    # Test that access token contains the correct payload
    token_data = jwt.token_data(token_pair.access_token)
    assert token_data is not None
    assert token_data.sub == staff_token_user.id
    assert token_data.email == staff_token_user.email
    assert token_data.is_verified == staff_token_user.is_verified
    # Test that staff is not admin
    assert token_data.is_admin is False
