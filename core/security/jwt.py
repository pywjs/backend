# core/security/jwt.py
import jwt as _jwt
from typing import Literal, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime, UTC, timedelta


class TokenUser(BaseModel):
    """A user object for token generation and verification. Allow passing of extra fields."""

    model_config = ConfigDict(extra="allow")
    id: str
    email: str | None = None
    is_verified: bool | None = False
    is_active: bool | None = False
    is_staff: bool | None = False
    is_admin: bool | None = False


class TokenPair(BaseModel):
    access: str
    refresh: str


class JWTTokenPayload(BaseModel):
    """A JWT token payload, requires minimum fields to be valid."""

    model_config = ConfigDict(extra="allow")
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

    def create_token(
        self,
        data: TokenUser,
        type: Literal["access", "refresh", "verification", "pair"] = "access",
    ):
        if type == "access":
            return self._create_access_token(data)
        elif type == "refresh":
            return self._create_refresh_token(data)
        elif type == "verification":
            return self._create_verification_token(data)
        elif type == "pair":
            access_token = self._create_access_token(data)
            refresh_token = self._create_refresh_token(data)
            return TokenPair(access=access_token, refresh=refresh_token)
        else:
            raise ValueError("Invalid token type")

    def token_data(self, token: str) -> TokenUser:
        payload = self._decode_jwt(token)
        return TokenUser(**payload)

    def _encode_jwt(self, payload: dict[str, Any]) -> str:
        return _jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def _decode_jwt(self, token: str) -> dict[str, Any]:
        try:
            payload = _jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload
        except _jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except _jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def _create_jwt_token(self, data: JWTTokenPayload, expire_delta: timedelta) -> str:
        data = data.model_dump()
        iat = datetime.now(UTC)
        exp = iat + expire_delta
        data.update({"iat": iat, "exp": exp})
        return self._encode_jwt(data)

    def _create_access_token(self, data: TokenUser) -> str:
        """
        Create an access token for the user.
        :param data: TokenData, includes: user_id, email, is_verified, is_active, is_staff, is_admin
        :return:
        """
        data = data.model_dump()
        data.update(
            {
                "type": "access",
            }
        )
        expire_delta = timedelta(minutes=self.access_token_expire_minutes)
        return self._create_jwt_token(data, expire_delta)

    def _create_refresh_token(self, data: TokenUser) -> str:
        data = data.model_dump()
        data.update(
            {
                "type": "refresh",
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
        data = data.model_dump()
        data.update(
            {
                "type": "verification",
            }
        )
        expire_delta = timedelta(minutes=self.verification_token_expire_minutes)
        return self._create_jwt_token(data, expire_delta)
