import uuid

from jose import JWTError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.enums import AuthFlow, UserRole
from app.core.exceptions import UnauthorizedError
from app.models.company import Company
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserRead


def _make_token_response(
    sub: str,
    flow: AuthFlow,
    user: UserRead | None,
    refresh_token: str | None = None,
) -> TokenResponse:
    return TokenResponse(
        access_token=security.create_access_token(sub, flow),
        refresh_token=refresh_token or security.create_refresh_token(sub, flow),
        flow=flow,
        user=user,
    )


def login_with_google(db: Session, google_id_token: str) -> TokenResponse:
    try:
        info = security.verify_google_token(google_id_token)
    except ValueError:
        raise UnauthorizedError("Token de Google inválido")

    user = crud.user.get_user_by_email(db, info["email"])

    if user is None:
        return _make_token_response(sub=info["email"], flow=AuthFlow.new_company, user=None)

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
        return _make_token_response(sub=sub, flow=flow, user=None, refresh_token=refresh_token)

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


def register_new_company(db: Session, email: str, data: RegisterRequest) -> tuple[Company, User]:
    company = Company(
        name=data.company_name,
        sector_id=data.sector_id,
        employee_range_id=data.employee_range_id,
        district_id=data.district_id,
        branch_count=data.branch_count,
    )
    db.add(company)
    db.flush()  # get company.id before committing

    user = User(
        name=data.name,
        email=email,
        job_title=data.job_title,
        role=UserRole.company_rep,
        company_id=company.id,
    )
    db.add(user)
    db.commit()
    db.refresh(company)
    db.refresh(user)
    return company, user


def complete_registration(db: Session, email: str, data: RegisterRequest) -> TokenResponse:
    _, user = register_new_company(db, email=email, data=data)
    return _make_token_response(
        sub=str(user.id),
        flow=AuthFlow.existing_company,
        user=UserRead.model_validate(user),
    )
