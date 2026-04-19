import uuid
from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core import security
from app.core.enums import AuthFlow
from app.core.exceptions import UnauthorizedError
from app.db.session import SessionLocal
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = security.decode_access_token(credentials.credentials)
    except (JWTError, ValueError):
        raise UnauthorizedError("Token inválido o expirado")

    if AuthFlow(payload.get("flow")) == AuthFlow.new_company:
        raise UnauthorizedError("Registro de empresa incompleto")

    from app import crud
    user = crud.user.get_user(db, uuid.UUID(payload["sub"]))
    return user
