from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_valid_token
from app.core.config import settings
from app.core.enums import AuthFlow
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import GoogleTokenRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.services.auth import complete_registration, login_with_google, refresh_tokens

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=TokenResponse)
def google_login(body: GoogleTokenRequest, db: Session = Depends(get_db)):
    return login_with_google(db, body.id_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    return refresh_tokens(db, body.refresh_token)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register_company(
    body: RegisterRequest,
    payload: dict = Depends(require_valid_token),
    db: Session = Depends(get_db),
):
    if AuthFlow(payload.get("flow")) != AuthFlow.new_company:
        raise UnauthorizedError("Este endpoint solo es válido para el flujo de nueva empresa")
    return complete_registration(db, email=payload["sub"], data=body)


class TokenDebugRequest(BaseModel):
    token: str


@router.post("/debug/decode")
def debug_decode_token(body: TokenDebugRequest) -> dict:
    from datetime import datetime, timezone
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
