import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import JWTError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.core import security
from app.core.config import settings
from app.core.enums import AuthFlow, UserRole
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import GoogleTokenRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


def _make_token_response(sub: str, flow: AuthFlow, user: UserRead | None, refresh_token: str | None = None) -> TokenResponse:
    return TokenResponse(
        access_token=security.create_access_token(sub, flow),
        refresh_token=refresh_token or security.create_refresh_token(sub, flow),
        flow=flow,
        user=user,
    )


@router.post("/google", response_model=TokenResponse)
def google_login(body: GoogleTokenRequest, db: Session = Depends(get_db)):
    try:
        info = security.verify_google_token(body.id_token)
    except ValueError:
        raise UnauthorizedError("Token de Google inválido")

    user = crud.user.get_user_by_email(db, info["email"])

    if user is None:
        return _make_token_response(
            sub=info["email"],
            flow=AuthFlow.new_company,
            user=None,
        )

    flow = AuthFlow.expert if user.role == UserRole.expert else AuthFlow.existing_company
    return _make_token_response(
        sub=str(user.id),
        flow=flow,
        user=UserRead.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = security.decode_refresh_token(body.refresh_token)
    except (JWTError, ValueError):
        raise UnauthorizedError("Refresh token inválido o expirado")

    sub = payload["sub"]
    flow = AuthFlow(payload["flow"])

    if flow == AuthFlow.new_company:
        return _make_token_response(sub=sub, flow=flow, user=None, refresh_token=body.refresh_token)

    try:
        user = crud.user.get_user(db, uuid.UUID(sub))
    except NoResultFound:
        raise UnauthorizedError("Usuario no encontrado")

    return _make_token_response(
        sub=sub,
        flow=flow,
        user=UserRead.model_validate(user),
        refresh_token=body.refresh_token,
    )


class TokenDebugRequest(BaseModel):
    token: str


@router.post("/debug/decode")
def debug_decode_token(body: TokenDebugRequest) -> dict:
    from datetime import datetime, timezone
    from jose import jwt
    try:
        payload = jwt.decode(
            body.token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        if "exp" in payload:
            exp_dt = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            payload["exp_human"] = exp_dt.isoformat()
            payload["expired"] = exp_dt < datetime.now(timezone.utc)
        return payload
    except (JWTError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))
