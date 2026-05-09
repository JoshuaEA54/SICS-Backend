from pydantic import BaseModel

from app.core.enums import AuthFlow
from app.schemas.user import UserRead


class GoogleTokenRequest(BaseModel):
    credential: str


class RefreshRequest(BaseModel):
    refresh_token: str


class GoogleProfile(BaseModel):
    name: str
    email: str
    picture: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    flow: AuthFlow
    user: UserRead | None = None
    google_profile: GoogleProfile | None = None


class RegisterRequest(BaseModel):
    name: str
    job_title: str
