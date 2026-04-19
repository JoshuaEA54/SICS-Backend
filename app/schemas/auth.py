from pydantic import BaseModel

from app.core.enums import AuthFlow
from app.schemas.user import UserRead


class GoogleTokenRequest(BaseModel):
    id_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    flow: AuthFlow
    user: UserRead | None = None
