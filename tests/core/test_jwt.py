# tests/core/test_jwt.py
import pytest
from core.security.jwt import JWT, TokenUser, TokenPair


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
