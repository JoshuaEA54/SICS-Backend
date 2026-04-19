from datetime import datetime, timedelta, timezone

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from jose import jwt

from app.core.config import settings
from app.core.enums import AuthFlow

_ACCESS = "access"
_REFRESH = "refresh"


def verify_google_token(token: str) -> dict:
    return id_token.verify_oauth2_token(
        token,
        google_requests.Request(),
        settings.GOOGLE_CLIENT_ID,
    )


def create_access_token(sub: str, flow: AuthFlow) -> str:
    payload = {
        "sub": sub,
        "type": _ACCESS,
        "flow": flow,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(sub: str, flow: AuthFlow) -> str:
    payload = {
        "sub": sub,
        "type": _REFRESH,
        "flow": flow,
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    if payload.get("type") != _ACCESS:
        raise ValueError("Not an access token")
    return payload


def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    if payload.get("type") != _REFRESH:
        raise ValueError("Not a refresh token")
    return payload
