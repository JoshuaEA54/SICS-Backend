import uuid

from jose import JWTError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.enums import AuthFlow, UserRole
from app.core.exceptions import UnauthorizedError
from app.models.user import User
from app.schemas.auth import GoogleProfile, RegisterRequest, TokenResponse
from app.schemas.company import CompanyCreate
from app.schemas.user import UserRead


def _make_token_response(
    sub: str,
    flow: AuthFlow,
    user: UserRead | None,
    refresh_token: str | None = None,
    name: str | None = None,
) -> TokenResponse:
    return TokenResponse(
        access_token=security.create_access_token(sub, flow, name),
        refresh_token=refresh_token or security.create_refresh_token(sub, flow, name),
        flow=flow,
        user=user,
    )


def login_with_google(db: Session, google_id_token: str) -> TokenResponse:
    try:
        info = security.verify_google_token(google_id_token)
    except ValueError:
        raise UnauthorizedError("Token de Google inválido")

    user = crud.user.get_user_by_email(db, info["email"])
    profile = GoogleProfile(
        name=info.get("name", ""),
        email=info["email"],
        picture=info.get("picture"),
    )

    if user is None:
        # Usuario totalmente nuevo — sin registro en DB
        response = _make_token_response(
            sub=info["email"],
            flow=AuthFlow.new_company,
            user=None,
            name=info.get("name", ""),
        )
        response.google_profile = profile
        return response

    if user.job_title is None:
        # Paso 1 completado (empresa+usuario creados), paso 2 pendiente
        response = _make_token_response(
            sub=info["email"],
            flow=AuthFlow.new_company,
            user=UserRead.model_validate(user),
            name=info.get("name", ""),
        )
        response.google_profile = profile
        return response

    flow = AuthFlow.expert if user.role == UserRole.expert else AuthFlow.existing_company
    return _make_token_response(sub=str(user.id), flow=flow, user=UserRead.model_validate(user))


def refresh_tokens(db: Session, refresh_token: str) -> TokenResponse:
    try:
        payload = security.decode_refresh_token(refresh_token)
    except (JWTError, ValueError):
        raise UnauthorizedError("Refresh token inválido o expirado")

    sub = payload["sub"]
    flow = AuthFlow(payload["flow"])

    if flow == AuthFlow.new_company:
        user = crud.user.get_user_by_email(db, sub)
        return _make_token_response(
            sub=sub,
            flow=flow,
            user=UserRead.model_validate(user) if user else None,
            refresh_token=refresh_token,
            name=payload.get("name") or None,
        )

    try:
        user = crud.user.get_user(db, uuid.UUID(sub))
    except NoResultFound:
        raise UnauthorizedError("Usuario no encontrado")

    return _make_token_response(
        sub=sub,
        flow=flow,
        user=UserRead.model_validate(user),
        refresh_token=refresh_token,
    )


def create_company_and_user(db: Session, payload: dict, data: CompanyCreate) -> TokenResponse:
    email = payload["sub"]
    name = payload.get("name", "")
    company = crud.company.create_company(db, data)  # flush, no commit
    user = User(
        name=name,
        email=email,
        job_title=None,
        role=UserRole.company_rep,
        company_id=company.id,
    )
    db.add(user)
    db.commit()  # empresa + usuario en una sola transacción
    db.refresh(user)
    return _make_token_response(
        sub=email,
        flow=AuthFlow.new_company,
        user=UserRead.model_validate(user),
        name=name,
    )


def complete_registration(db: Session, email: str, data: RegisterRequest) -> TokenResponse:
    """Actualiza nombre y cargo del usuario existente (paso 2 del registro)."""
    user = crud.user.get_user_by_email(db, email)
    if user is None:
        raise UnauthorizedError("Usuario no encontrado")
    user.name = data.name
    user.job_title = data.job_title
    db.commit()
    db.refresh(user)
    return _make_token_response(
        sub=str(user.id),
        flow=AuthFlow.existing_company,
        user=UserRead.model_validate(user),
    )
