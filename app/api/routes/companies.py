import uuid

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
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

router = APIRouter(prefix="/companies", tags=["companies"])


# ── Sectors ───────────────────────────────────────────────────────────────────

@router.get("/sectors", response_model=Page[SectorRead])
def list_sectors(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_sectors_query())


@router.post("/sectors", response_model=SectorRead, status_code=201)
def create_sector(data: SectorCreate, db: Session = Depends(get_db)):
    return crud.company.create_sector(db, data)


@router.put("/sectors/{sector_id}", response_model=SectorRead)
def update_sector(sector_id: int, data: SectorUpdate, db: Session = Depends(get_db)):
    try:
        return crud.company.update_sector(db, sector_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Sector not found")


@router.delete("/sectors/{sector_id}", status_code=204)
def delete_sector(sector_id: int, db: Session = Depends(get_db)):
    try:
        crud.company.delete_sector(db, sector_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Sector not found")
    return Response(status_code=204)


# ── Employee Ranges ───────────────────────────────────────────────────────────

@router.get("/employee-ranges", response_model=Page[EmployeeRangeRead])
def list_employee_ranges(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_employee_ranges_query())


@router.post("/employee-ranges", response_model=EmployeeRangeRead, status_code=201)
def create_employee_range(data: EmployeeRangeCreate, db: Session = Depends(get_db)):
    return crud.company.create_employee_range(db, data)


@router.put("/employee-ranges/{range_id}", response_model=EmployeeRangeRead)
def update_employee_range(range_id: int, data: EmployeeRangeUpdate, db: Session = Depends(get_db)):
    try:
        return crud.company.update_employee_range(db, range_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Employee range not found")


@router.delete("/employee-ranges/{range_id}", status_code=204)
def delete_employee_range(range_id: int, db: Session = Depends(get_db)):
    try:
        crud.company.delete_employee_range(db, range_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Employee range not found")
    return Response(status_code=204)


# ── Companies ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=Page[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_companies_query())


@router.post("/", response_model=CompanyRead, status_code=201)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    return crud.company.create_company(db, data)


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    company = crud.company.get_company(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.put("/{company_id}", response_model=CompanyRead)
def update_company(company_id: uuid.UUID, data: CompanyUpdate, db: Session = Depends(get_db)):
    try:
        return crud.company.update_company(db, company_id, data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Company not found")


@router.delete("/{company_id}", status_code=204)
def delete_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        crud.company.delete_company(db, company_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Company not found")
    return Response(status_code=204)


# ── Contacts ──────────────────────────────────────────────────────────────────

@router.get("/{company_id}/contacts", response_model=Page[ContactRead])
def list_contacts(company_id: uuid.UUID, db: Session = Depends(get_db)):
    return paginate(db, crud.company.get_contacts_query(company_id))


@router.post("/{company_id}/contacts", response_model=ContactRead, status_code=201)
def create_contact(company_id: uuid.UUID, data: ContactCreate, db: Session = Depends(get_db)):
    data.company_id = company_id
    return crud.company.create_contact(db, data)


@router.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        crud.company.delete_contact(db, contact_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Contact not found")
    return Response(status_code=204)
