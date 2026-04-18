import uuid

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.company import Company, Contact, EmployeeRange, Sector
from app.schemas.company import (
    CompanyCreate,
    CompanyUpdate,
    ContactCreate,
    EmployeeRangeCreate,
    EmployeeRangeUpdate,
    SectorCreate,
    SectorUpdate,
)


# ── Sector ────────────────────────────────────────────────────────────────────

def get_sectors_query() -> Select:
    return select(Sector).order_by(Sector.name)


def create_sector(db: Session, data: SectorCreate) -> Sector:
    sector = Sector(name=data.name)
    db.add(sector)
    db.commit()
    db.refresh(sector)
    return sector


def update_sector(db: Session, sector_id: int, data: SectorUpdate) -> Sector:
    sector = db.execute(select(Sector).where(Sector.id == sector_id)).scalar_one()
    sector.name = data.name
    db.commit()
    db.refresh(sector)
    return sector


def delete_sector(db: Session, sector_id: int) -> None:
    sector = db.execute(select(Sector).where(Sector.id == sector_id)).scalar_one()
    db.delete(sector)
    db.commit()


# ── EmployeeRange ─────────────────────────────────────────────────────────────

def get_employee_ranges_query() -> Select:
    return select(EmployeeRange).order_by(EmployeeRange.id)


def create_employee_range(db: Session, data: EmployeeRangeCreate) -> EmployeeRange:
    er = EmployeeRange(label=data.label)
    db.add(er)
    db.commit()
    db.refresh(er)
    return er


def update_employee_range(db: Session, range_id: int, data: EmployeeRangeUpdate) -> EmployeeRange:
    er = db.execute(select(EmployeeRange).where(EmployeeRange.id == range_id)).scalar_one()
    er.label = data.label
    db.commit()
    db.refresh(er)
    return er


def delete_employee_range(db: Session, range_id: int) -> None:
    er = db.execute(select(EmployeeRange).where(EmployeeRange.id == range_id)).scalar_one()
    db.delete(er)
    db.commit()


# ── Company ───────────────────────────────────────────────────────────────────

def get_company(db: Session, company_id: uuid.UUID) -> Company:
    return db.execute(select(Company).where(Company.id == company_id)).scalar_one()


def get_companies_query() -> Select:
    return select(Company).order_by(Company.name)


def create_company(db: Session, data: CompanyCreate) -> Company:
    company = Company(
        name=data.name,
        sector_id=data.sector_id,
        employee_range_id=data.employee_range_id,
        district_id=data.district_id,
        branch_count=data.branch_count,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company_id: uuid.UUID, data: CompanyUpdate) -> Company:
    company = db.execute(select(Company).where(Company.id == company_id)).scalar_one()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: uuid.UUID) -> None:
    company = db.execute(select(Company).where(Company.id == company_id)).scalar_one()
    db.delete(company)
    db.commit()


# ── Contact ───────────────────────────────────────────────────────────────────

def get_contacts_query(company_id: uuid.UUID) -> Select:
    return select(Contact).where(Contact.company_id == company_id).order_by(Contact.name)


def create_contact(db: Session, data: ContactCreate) -> Contact:
    contact = Contact(
        company_id=data.company_id,
        name=data.name,
        email=str(data.email),
        job_title=data.job_title,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: uuid.UUID) -> None:
    contact = db.execute(select(Contact).where(Contact.id == contact_id)).scalar_one()
    db.delete(contact)
    db.commit()
