import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Company ───────────────────────────────────────────────────────────────────

class CompanyCreate(BaseModel):
    name: str
    sector_id: int
    employee_range_id: int
    district_id: int
    branch_count: int = 0


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
