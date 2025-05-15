# core/security/jwt.py

from datetime import datetime, timedelta, timezone
from typing import Literal, Any
import jwt


class JWTAuth:
    def __init__(
        self,
        secret: str,
        algorithm: Literal["HS256", "HS384", "HS512"] = "HS256",
        issuer: str | None = None,
        audience: str | None = None,
        access_token_expire_minutes: int = 30,
        refresh_token_expire_minutes: int = 60 * 24 * 7,
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.issuer = issuer
        self.audience = audience
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes

    def _create_token(
        self,
        subject: str,
        expires_delta: timedelta,
        kind: Literal["access", "refresh"] = "access",
        extra: dict[str, Any] | None = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + expires_delta,
            "kind": kind,
        }
        if self.issuer:
            payload["iss"] = self.issuer
        if self.audience:
            payload["aud"] = self.audience
        payload.update(extra or {})
        return self._encode(payload)

    def _encode(self, payload: dict) -> str:
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.algorithm,
        )

    def _decode(
        self, token: str, kind: Literal["access", "refresh"] | None = None
    ) -> dict:
        options = {"require": ["exp", "sub", "kind"]}
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options=options,
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

        # Check token type if specified
        if kind and payload.get("kind") != kind:
            raise ValueError(
                f"Invalid token type: expected {kind}, got {payload.get('kind')}"
            )

        return payload

    def create_access_token(self, subject: str, extra: dict | None = None) -> str:
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        return self._create_token(subject, expires_delta, "access", extra)

    def create_refresh_token(self, subject: str, extra: dict | None = None) -> str:
        expires_delta = timedelta(minutes=self.refresh_token_expire_minutes)
        return self._create_token(subject, expires_delta, "refresh", extra)

    def decode_token(
        self, token: str, kind: Literal["access", "refresh"] | None = None
    ) -> dict:
        return self._decode(token, kind)
