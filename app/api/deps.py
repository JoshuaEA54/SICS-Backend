from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core import security
from app.core.enums import AuthFlow, UserRole
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.db.session import SessionLocal
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_valid_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Validates the JWT without restricting the auth flow. Use for catalog endpoints accessible during registration."""
    try:
        return security.decode_access_token(credentials.credentials)
    except (JWTError, ValueError):
        raise UnauthorizedError("Token inválido o expirado")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = security.decode_access_token(credentials.credentials)
    except (JWTError, ValueError):
        raise UnauthorizedError("Token inválido o expirado")

    from app import crud
    user = crud.user.get_user_by_email(db, payload["sub"])
    if user is None:
        raise UnauthorizedError("Usuario no encontrado")
    return user


def require_expert(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.expert:
        raise ForbiddenError("Solo el experto puede realizar esta acción")
    return user


def require_company_rep(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.company_rep:
        raise ForbiddenError("Solo la empresa puede realizar esta acción")
    return user
