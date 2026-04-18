import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Sector ────────────────────────────────────────────────────────────────────

class SectorCreate(BaseModel):
    name: str


class SectorUpdate(BaseModel):
    name: str


class SectorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# ── Employee Range ────────────────────────────────────────────────────────────

class EmployeeRangeCreate(BaseModel):
    label: str


class EmployeeRangeUpdate(BaseModel):
    label: str


class EmployeeRangeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str


# ── Company ───────────────────────────────────────────────────────────────────

class CompanyCreate(BaseModel):
    name: str
    sector_id: int
    employee_range_id: int
    district_id: int
    branch_count: int = 0


class CompanyUpdate(BaseModel):
    name: str | None = None
    sector_id: int | None = None
    employee_range_id: int | None = None
    district_id: int | None = None
    branch_count: int | None = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    sector_id: int
    employee_range_id: int
    district_id: int
    branch_count: int
    created_at: datetime


# ── Contact ───────────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    company_id: uuid.UUID
    name: str
    email: EmailStr
    job_title: str | None = None


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    email: EmailStr
    job_title: str | None
    created_at: datetime
