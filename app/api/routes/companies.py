import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user, get_db, require_valid_token
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import TokenResponse
from app.schemas.company import (
    CompanyCreate,
    CompanyRead,
    CompanyUpdate,
    ContactCreate,
    ContactRead,
    EmployeeRangeCreate,
    EmployeeRangeRead,
    EmployeeRangeUpdate,
    SectorCreate,
    SectorRead,
    SectorUpdate,
)
from app.services.auth import create_company_and_user

router = APIRouter(prefix="/companies", tags=["companies"], dependencies=[Depends(get_current_user)])

# Router for catalog endpoints accessible during company registration (new_company flow)
catalog_router = APIRouter(prefix="/companies", tags=["companies"], dependencies=[Depends(require_valid_token)])


# ── Sectors ───────────────────────────────────────────────────────────────────

@catalog_router.get("/sectors", response_model=Page[SectorRead])
def list_sectors(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_sectors_query())


@router.post("/sectors", response_model=SectorRead, status_code=HTTPStatus.CREATED)
def create_sector(data: SectorCreate, db: Session = Depends(get_db)):
    return crud.company.create_sector(db, data)


@router.put("/sectors/{sector_id}", response_model=SectorRead)
def update_sector(sector_id: int, data: SectorUpdate, db: Session = Depends(get_db)):
    return crud.company.update_sector(db, sector_id, data)


@router.delete("/sectors/{sector_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_sector(sector_id: int, db: Session = Depends(get_db)):
    crud.company.delete_sector(db, sector_id)


# ── Employee Ranges ───────────────────────────────────────────────────────────

@catalog_router.get("/employee-ranges", response_model=Page[EmployeeRangeRead])
def list_employee_ranges(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_employee_ranges_query())


@catalog_router.post("/", response_model=TokenResponse, status_code=HTTPStatus.CREATED)
def create_company(data: CompanyCreate, payload: dict = Depends(require_valid_token), db: Session = Depends(get_db)):
    return create_company_and_user(db, payload=payload, data=data)


@router.post("/employee-ranges", response_model=EmployeeRangeRead, status_code=HTTPStatus.CREATED)
def create_employee_range(data: EmployeeRangeCreate, db: Session = Depends(get_db)):
    return crud.company.create_employee_range(db, data)


@router.put("/employee-ranges/{range_id}", response_model=EmployeeRangeRead)
def update_employee_range(range_id: int, data: EmployeeRangeUpdate, db: Session = Depends(get_db)):
    return crud.company.update_employee_range(db, range_id, data)


@router.delete("/employee-ranges/{range_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_employee_range(range_id: int, db: Session = Depends(get_db)):
    crud.company.delete_employee_range(db, range_id)


# ── Companies ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_companies_query())



@catalog_router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    return crud.company.get_company(db, company_id)


@catalog_router.put("/{company_id}", response_model=CompanyRead)
def update_company(company_id: uuid.UUID, data: CompanyUpdate, payload: dict = Depends(require_valid_token), db: Session = Depends(get_db)):
    sub = payload["sub"]
    try:
        user = crud.user.get_user(db, uuid.UUID(sub))
    except Exception:
        user = crud.user.get_user_by_email(db, sub)
    if user is None or str(user.company_id) != str(company_id):
        raise UnauthorizedError("No autorizado para modificar esta empresa")
    return crud.company.update_company(db, company_id, data)


@router.delete("/{company_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    crud.company.delete_company(db, company_id)


# ── Contacts ──────────────────────────────────────────────────────────────────

@router.get("/{company_id}/contacts", response_model=Page[ContactRead])
def list_contacts(company_id: uuid.UUID, db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_contacts_query(company_id))


@router.post("/{company_id}/contacts", response_model=ContactRead, status_code=HTTPStatus.CREATED)
def create_contact(company_id: uuid.UUID, data: ContactCreate, db: Session = Depends(get_db)):
    return crud.company.create_contact(db, company_id, data)


@router.delete("/contacts/{contact_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_contact(contact_id: uuid.UUID, db: Session = Depends(get_db)):
    crud.company.delete_contact(db, contact_id)
