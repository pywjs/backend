# core/security/jwt.py
import jwt as _jwt
from typing import Literal, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime, UTC, timedelta


from .exceptions import InvalidTokenException, ExpiredTokenException


class TokenUser(BaseModel):
    """A user object for token generation and verification. Allow passing of extra fields."""

    model_config = ConfigDict(extra="allow")
    id: str
    email: str | None = None
    is_verified: bool | None = False
    is_active: bool | None = False
    is_staff: bool | None = False
    is_admin: bool | None = False

    @property
    def sub(self) -> str:
        return str(self.id)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerificationToken(BaseModel):
    code: str
    token_type: str = "bearer"


class JWTTokenPayload(BaseModel):
    """A JWT token payload, requires minimum fields to be valid."""

    model_config = ConfigDict(
        extra="allow",
    )
    sub: str
    iat: datetime | int
    exp: datetime | int


class JWT:
    def __init__(
        self,
        secret: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,  # 30 minutes
        refresh_token_expire_minutes: int = 60 * 24 * 7,  # 7 days
        verification_token_expire_minutes: int = 5,  # 5 minutes
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        self.verification_token_expire_minutes = verification_token_expire_minutes

    def access_token(self, data: TokenUser) -> str:
        """
        Create an access token for the user.
        """
        return self._create_access_token(data)

    def refresh_token(self, data: TokenUser) -> str:
        """
        Create a refresh token for the user.
        """
        return self._create_refresh_token(data)

    def verification_token(self, data: TokenUser) -> VerificationToken:
        """
        Create a verification token for the user.
        """
        return VerificationToken(code=self._create_verification_token(data))

    def token_pair(self, data: TokenUser) -> TokenPair:
        """
        Create a pair of access and refresh tokens for the user.
        """
        return TokenPair(
            access_token=self._create_access_token(data),
            refresh_token=self._create_refresh_token(data),
        )

    def token_data(self, token: str) -> TokenUser:
        payload = self._decode_jwt(token)
        return TokenUser(**payload)

    def verify(
        self,
        token: str,
        token_type: Literal["access", "refresh", "verification", "pair"] = "refresh",
    ) -> bool:
        try:
            payload = self._decode_jwt(token)
            if token_type == "access":
                return payload.get("token_type") == "access"
            elif token_type == "refresh":
                return payload.get("token_type") == "refresh"
            elif token_type == "verification":
                return payload.get("token_type") == "verification"
            elif token_type == "pair":
                return payload.get("token_type") in ["access", "refresh"]
            else:
                raise ValueError(f"Invalid token_type: {token_type}")
        except ValueError:
            return False

    def _encode_jwt(self, payload: JWTTokenPayload) -> str:
        return _jwt.encode(payload.model_dump(), self.secret, algorithm=self.algorithm)

    def _decode_jwt(self, token: str) -> dict[str, Any]:
        try:
            payload = _jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except _jwt.ExpiredSignatureError:
            raise ExpiredTokenException
        except _jwt.InvalidTokenError:
            raise InvalidTokenException

    def _create_jwt_token(self, data: dict[str, Any], expire_delta: timedelta) -> str:
        sub = data.get("id")
        iat = datetime.now(UTC)
        exp = iat + expire_delta
        payload = JWTTokenPayload.model_construct(sub=sub, iat=iat, exp=exp, **data)
        return self._encode_jwt(payload)

    def _create_access_token(self, data: TokenUser) -> str:
        """
        Create an access token for the user.
        :param data: TokenData, includes: user_id, email, is_verified, is_active, is_staff, is_admin
        :return:
        """
        data = data.model_dump()
        data.update(
            {
                "token_type": "access",
            }
        )
        expire_delta = timedelta(minutes=self.access_token_expire_minutes)
        return self._create_jwt_token(data, expire_delta)

    def _create_refresh_token(self, data: TokenUser) -> str:
        """Create a minimal refresh token for the user, only include sub, iat, exp and token_type."""
        data = data.model_dump(include={"id"})  # we only need the ID from the TokenUser
        data.update(
            {
                "token_type": "refresh",
            }
        )
        expire_delta = timedelta(minutes=self.refresh_token_expire_minutes)
        return self._create_jwt_token(data, expire_delta)

    def _create_verification_token(self, data: TokenUser) -> str:
        """
        Create a verification token for the user.
        :param data: TokenData, includes: user_id, email, is_verified, is_active, is_staff, is_admin
        :return:
        """
        data = data.model_dump(include={"id"})
        data.update({"token_type": "verification"})
        expire_delta = timedelta(minutes=self.verification_token_expire_minutes)
        return self._create_jwt_token(data, expire_delta)
